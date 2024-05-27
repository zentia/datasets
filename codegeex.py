from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained("THUDM/codegeex2-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/codegeex2-6b", trust_remote_code=True, device='cuda')
model = model.eval()

# remember adding a language tag for better performance
prompt = '''
// Lua代码翻译为TypeScript
/*
ChartsAction = {
    ExitCharts = "ExitCharts",      -- 退出排行榜

    RefreshLocation = "RefreshLocation",    -- 切换战区

    SelectBattleArea = "SelectBattleArea",          -- 天梯榜选择战区
    
    SelectLordID = "SelectLordID",  -- 棋手榜切换棋手
    OpenSelectLordBattleArea = "OpenSelectLordBattleArea",   -- 棋手榜选择战区
    SelectLordBattleArea = "SelectLordBattleArea",   -- 切换棋手区域
    ConfirmLordBattleArea = "ConfirmLordBattleArea",  -- 确认选择棋手区域

    JumpToRankIndex = "JumpToRankIndex",  -- 跳转到某个名次

    QueryRankScoreData = "QueryRankScoreData", --请求天梯排行数据
    QueryLordScoreData = "QueryLordScoreData", --请求棋手排行数据
    ReqChangeBattleArea = "ReqChangeBattleArea",  --请求更换战区
    QueryFriendChartsInfo = "QueryFriendChartsInfo", --请求好友榜数据
    QueryFriendLeaderboardPlace = "QueryFriendLeaderboardPlace", --请求好友类型排名
    QueryLordRankPlace = "QueryLordRankPlace", --请求棋手的排名信息
    
    -- SelectCharts = "SelectCharts",
    -- SelectSeason = "SelectSeason",
    -- SelectRankType = "SelectRankType",

    -- CreatSelectChoessListUI ="CreatSelectChoessListUI" ,
    -- AddressRankTypeSelect = "AddressRankTypeSelect",
}

ChartsUpdateUI = {
    RefreshCurrentCharts = "RefreshCurrentCharts",   -- 刷新当前的榜单界面（比如在调整战区之后）

    LordConfirmLordBattleArea = "LordConfirmLordBattleArea", -- 由Mediator传下来的确认选择战区

    RefreshChartsContent = "RefreshChartsContent", --刷新排行榜
    RefreshChartsLordScore = "RefreshChartsLordScore", --刷新棋手排行
    ChangeBattleAreaSuccess = "ChangeBattleAreaSuccess", --战区切换成功
    RefreshFriendChartsInfo = "RefreshFriendChartsInfo", --刷新好友榜单数据
    QueryFriendLBPlaceOver = "QueryFriendLBPlaceOver",  --好友类型榜单获取完成
    RefreshLordRankPlace = "RefreshLordRankPlace",  --刷新棋手排名信息
}

CanRequestMoreInfoState = 
{
    CanRequest              = 0, --可以请求
    AlreadyHasData          = 1, --已经拥有数据
}

QueryChartInfoResultType = 
{
    QueryResult_Success     = 0, --获取成功

    QueryResult_NoData      = 2, --没有数据
    QueryResult_ServerError = 3, --服务器报错
    QueryResult_UnknowError = 10, --未知错误
}

ChartsOprationType = {
    VisitPeople = 1,
    AddFriend = 2,
}
*/
'''
inputs = tokenizer.encode(prompt, return_tensors="pt").to(model.device)
outputs = model.generate(inputs, max_length=1024*2, top_k=1)
response = tokenizer.decode(outputs[0])
print(response)
