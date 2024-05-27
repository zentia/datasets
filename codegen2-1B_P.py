from transformers import AutoTokenizer, AutoModelForCausalLM
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codegen2-1B")
model = AutoModelForCausalLM.from_pretrained("Salesforce/codegen2-1B", trust_remote_code=True, revision="main")

text = """
Lua translated to TypeScript
Lua:

local klass = import("/Common/OOP/Class")

EnumBegin(1)
---@enum BeginloadGenType
BeginloadGenType = 
{
    DefaultOfflineParam = NextEnum(),
    MassiveOfflineParam = NextEnum(),
    AIChallenge = NextEnum(),
    Newbie = NextEnum(),
    Lobby = NextEnum(),
}
BeginloadGenType = EnumEnd(BeginloadGenType)

---@alias OfflineParam Assets.Scripts.GameLogic.OfflineParam
---@alias DebugPlayerInfo Assets.Scripts.GameLogic.DebugPlayerInfo

---@class OfflineBattleServiceClass
local OfflineBattleServiceClass = DeclareClass("OfflineBattleServiceClass")

function OfflineBattleServiceClass:ctor()
    self._components = {} ---@type OfflineBattleComponentBaseClass[]
    
    self.decoded = false ---@type DecodedLockSptepRecordFile
    self.hostPlayeIdx = 1
    self.recoverFrameNoType = false ---@type RecoverFrameNoType

    self.curRecordPath = false ---@type string
    self.isStartingGame = false
end


function OfflineBattleServiceClass:GetComponents()
    return self._components
end

---@param genType BeginloadGenType
---@param userData any
---@return boolean
function OfflineBattleServiceClass:StartGame(genType, userData)
    if self.isStartingGame then
        LogE('BattleProcess', 'OfflineBattleService::StartGame() fail: isStartingGame == true')
        return false
    end

    if StateService:IsSwitching() then
        LogE('BattleProcess', 'OfflineBattleService::StartGame() fail: gameplayState is switching, %d', genType)
        return false
    end

    local beginloadComponent = OfflineBattleComponentFactory:CreateBeginloadComponent(genType)
    beginloadComponent:vAwake()
    local beginloadData = beginloadComponent:vGenerateBeginLoadData(userData)
    if not beginloadData then
        LogE('BattleProcess', 'OfflineBattleService::StartGame() generate beginload data failed: %d', genType)
        return false
    end
    beginloadComponent:vPrepare(beginloadData)
    self.isStartingGame = true
    BeginloadService:Clear()
    
    self:ResetComponents()
    table.append(self._components, beginloadComponent)

    self.hostPlayeIdx = 1
    BeginloadService:SetOnBeginloadArrivedCB(self.OnBeginLoad)
    ---@downcast
    ---@type OSProto.SCPVPGameBeginLoad.ntf
    local body = {
        BeginLoadData = beginloadData
    }
    self:EmitBeginLoadNtf(body)
    return true
end

---@param decoded DecodedLockSptepRecordFile
---@param beginLoadNtf OSProto.SCPVPGameBeginLoad.ntf
---@param selectHostPlayerIndex number
---@param recoverFrameNoType RecoverFrameNoType
---@return boolean
function OfflineBattleServiceClass:StartGameByRecover(decoded, beginLoadNtf, selectHostPlayerIndex, recoverFrameNoType)
    if not beginLoadNtf then
        return
    end

    BeginloadService:Clear()
    self.decoded = decoded
    self.hostPlayeIdx = selectHostPlayerIndex or 1
    self.recoverFrameNoType = recoverFrameNoType
    
    GamePlayGlobalHandler:SetBattleRecovering(true)
    
    GameplayHelper:SetIsOfflineBattle(true)

    BeginloadService:SetOnBeginloadArrivedCB(self.OnBeginLoad)

    self:EmitBeginLoadNtf(beginLoadNtf)

    return true
end

---@param beginLoadNtf OSProto.SCPVPGameBeginLoad.ntf
function OfflineBattleServiceClass:EmitBeginLoadNtf(beginLoadNtf)
    ---@type MockerNotification
    local ntf = {
        MsgID = SCNotificationTypes.SCPVPGameBeginLoad,
        Body = beginLoadNtf
    }
    NetworkMocker:EmitNtf(ntf)
end

auto_bind()
---@param serverNtf OSProto.SCPVPGameBeginLoad.ntf
function OfflineBattleServiceClass:OnBeginLoad(serverNtf)
    self.isStartingGame = false

    BeginloadService:SetOnBeginloadArrivedCB(false)

    ReplayService:SetRelaySvrParamForMocker(serverNtf.BeginLoadData)

    
    FrameCommandService:SetConnectType(FrameConnectType.Relay) 

    local newComponents = {}
    OfflineBattleComponentFactory:CreateComponents(serverNtf.BeginLoadData.PlayModID, newComponents)
    for _,component in pairs(newComponents) do
        component:vAwake()
        table.append(self._components, component)
    end
    
    if serverNtf.RoundRecoverInfo then
        self:SetRelayMockerRecoverInfo(self.decoded, serverNtf.RoundRecoverInfo, self.recoverFrameNoType)
        GamePlayGlobalHandler:SetBattleRecovering(true)
    end
    local deskPlayerInfo = serverNtf.BeginLoadData.PlayerInfo
    if deskPlayerInfo and deskPlayerInfo.PlayerInfos and not table.empty(deskPlayerInfo.PlayerInfos) then
        local playInfo = deskPlayerInfo.PlayerInfos[self.hostPlayeIdx].PlayerInfo
        LuaSetGameWatchOBMode(ObMode.None, playInfo.ObjId, GamePlayerCenter:GetPlayerUID(playInfo))
    end
    self:RegisterEvent()
    local levelContext
    local beginLoadDataComponent = self:GetComponent(ClassLib.LobbyBattleBeginLoadDataComponentClass)
    if beginLoadDataComponent then
        levelContext = beginLoadDataComponent:vGenerateLevelContext()
    end
    BeginloadService:DefaultBeginloadHandler(serverNtf, levelContext)
    return true
end

---@param recordPath string
function OfflineBattleServiceClass:SetRecordPath(recordPath)
    self.curRecordPath = recordPath
end

---@return string
function OfflineBattleServiceClass:GetRecordPath()
    return self.curRecordPath
end

---@param round number
function OfflineBattleServiceClass:GMBackToRound(round)
    local startRound = BeginloadService:GetBeginLoadData().StartRoundNum
    local fromRound = round
    if round < startRound then
        fromRound = 0
    end

    if FrameCommandService:IsProcessingRecover() then
        Bubble:ShowLocalizeString("SwichRounding")
        return
    end

    if FrameCommandService:IsGameCorePaused() then
        Bubble:Show("gamecore is paused")
        return
    end

    local decoded = ReplayService.DecodeReplay(self.curRecordPath)
    if not decoded then
        Bubble:Show(string.format("%s decode faild", self.curRecordPath))
        return
    end
   
    ---@type OSProto.SCPVPGameBeginLoad.ntf
    local beginLoadNtf = ReplayService:ExtractRecoverData(decoded, fromRound)
    if beginLoadNtf then
        if not beginLoadNtf.RoundRecoverInfo and fromRound == 0 then
            beginLoadNtf.RoundRecoverInfo = {} 
        end
        if beginLoadNtf.RoundRecoverInfo then
            self:BackToRound(decoded, beginLoadNtf.RoundRecoverInfo)
        else
            local targetRound = fromRound == 0 and startRound or round + 1
            Bubble:Show(string.format("back to round %d failed", targetRound))
        end
    end
end

---@param decoded DecodedLockSptepRecordFile
---@param roundRecoverInfo OSProto.STPVPRoundRecoverInfo 
---@return boolean
function OfflineBattleServiceClass:BackToRound(decoded, roundRecoverInfo)
    self:SetRelayMockerRecoverInfo(decoded, roundRecoverInfo, RecoverFrameNoType.RoundFrameNo)
    
    local recordPath = ReplayService:GenReplayPath(decoded.BeginLoadData, true)
    self:SetRecordPath(recordPath)
    
    --step1:重启gamecore
    lua2cpp.SliceRebootGameCoreOut(roundRecoverInfo.LastestSavePoint ~= nil, recordPath)
    --step2:重启c# Battle
    CS.Assets.Scripts.Framework.CSRecoverSys.GetInstance():SetNeedRebootClient(true)
    --step3:清理帧号
    FrameCommandService:ResetWindow()
    FrameCommandService:ResetData()

    if roundRecoverInfo.latestRound then
        LockInput:Lock("SwitchRoundInGame", {delay = 3.0})
        --step4:设置恢复信息
        FrameCommandService:SetRecoverInfo(roundRecoverInfo)
        FrameCommandService:ApplyRecoverData(false)
        FrameCommandService:RequestRelaySyncCacheFrames()
    else
        --step4:追帧
        CS.SGW.StartCSRecoverChaseUp(0, true)
    end
end

event(LuaEventID.ChaseFrameOver)
function OfflineBattleServiceClass:OnChaseFrameOver()
    LockInput:Unlock("SwitchRoundInGame")
end

---@param decoded DecodedLockSptepRecordFile
---@param roundRecoverInfo OSProto.STPVPRoundRecoverInfo 
---@param recoverFrameNoType RecoverFrameNoType
function OfflineBattleServiceClass:SetRelayMockerRecoverInfo(decoded, roundRecoverInfo, recoverFrameNoType)
    ---@type OfflineBattleDefaultRelayMockerComponentClass
    local comp = self:GetComponent(ClassLib.OfflineBattleDefaultRelayMockerComponentClass)
    if comp then
        comp:SetRecoverData(decoded, roundRecoverInfo, recoverFrameNoType)
    end
end

function OfflineBattleServiceClass:GetComponent(subClass)
    for _, component in pairs(self._components) do
        if klass.IsSubClass(component.class, subClass) then
            return component
        end
    end
end

---@param playMod ResData.PLAYMOD_TYPE_Keys
function OfflineBattleServiceClass:CantHandle(playModID)
    local playModConf = PBDataManager.ResPlayMod.Get(playModID)

    return table.contains(self._CantHandlePlayModGroupType, playModConf.SubGroup)
end

function OfflineBattleServiceClass:RegisterEvent()
    EventService:AddEvent(LuaEventID.LeaveFromBattle, self.OnLeaveFramBattle)
end

function OfflineBattleServiceClass:UnregisterEvent()
    EventService:RemoveEvent(LuaEventID.LeaveFromBattle, self.OnLeaveFramBattle)
end

auto_bind()
function OfflineBattleServiceClass:OnLeaveFramBattle()
    self:UnregisterEvent()
    self:ResetComponents()
    if GameplayHelper:GetIsOfflineBattle() then
        GameplayHelper:SetIsOfflineBattle(false)
    end

    self.decoded = false
    self.hostPlayeIdx = 1
end

function OfflineBattleServiceClass:ResetComponents()
    for _,component in pairs(self._components) do
        component:vDestroy()
    end

    table.clear(self._components)
end


---------------响应离线面板-----------------------------

async() 
event(LuaEventID.StartOfflineBattleGame)
---@param param StartOfflineBattleGameParam
function OfflineBattleServiceClass:OnStartOfflineBattleGame(param)
    local offlineParam = table.trivial(param.param) ---@type OfflineParam
    
    BeginloadService:Clear()
    
    if offlineParam.openBroadcast then
        CS.Assets.Scripts.UI.InTheGame.Standard.UIPickCard.DebugForShowEffect = true
    end
    
    local playModID = offlineParam.playModID
    if CommonUtility:IsPlayModInGroup(playModID, ResData.PLAYMOD_GROUP_TYPE.MASSIVE) then
        self:StartGame(BeginloadGenType.MassiveOfflineParam, offlineParam)
    elseif CommonUtility:IsPlayModInGroup(playModID, ResData.PLAYMOD_GROUP_TYPE.AICHALLENGE) then
        self:StartGame(BeginloadGenType.AIChallenge, offlineParam)
    elseif CommonUtility:IsPlayModInGroup(playModID, ResData.PLAYMOD_GROUP_TYPE.TUTORIAL) or CommonUtility:IsPlayModInGroup(playModID, ResData.PLAYMOD_GROUP_TYPE.SLICE) then
        self:StartGame(BeginloadGenType.Newbie, offlineParam)
    else
        self:StartGame(BeginloadGenType.DefaultOfflineParam, offlineParam)
    end
end

---@type OfflineBattleServiceClass
OfflineBattleService = ClassLib.OfflineBattleServiceClass.new()
TypeScript:
                                                
"""
input_ids = tokenizer(text, return_tensors="pt").input_ids
generated_ids = model.generate(input_ids, max_length=1024*10)
print(tokenizer.decode(generated_ids[0], skip_special_tokens=True))
