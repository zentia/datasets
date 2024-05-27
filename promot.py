# Lua翻译成TypeScript，遵循以下规则
# 1.在文件的顶部，添加以下内容：
#   /* eslint-disable camelcase */
#   /* eslint-disable @typescript-eslint/naming-convention */
# 2.ClassLib.XXX表示后面的XXX是一个class，翻译之后只用保留XXX，不要保留ClassLib
# 3.DeclareClass表示定义一个类，第一个参数是类名，第二个参数是基类名,如果没有指定基类名，则使用OSObject作为基类名
# 4.ctor是Lua的构造函数，如果TypeScript的constructor内容为空，不要保留这些内容
# 5.在ctor函数里面出现的self.的赋值语句，是成员字段的定义。
# 6.所有TypeScript的成员字段和函数，添加public修饰符
# 7.LogD/LogI/LogW/LogE分别替换为Log.debug/Log.info/Log.warn/Log.error
# 8.Lua里面出现在函数前面的data_watch/ui_event/event是装饰器
# 9.async()替换为async
# 10.self:Async替换为async
# 11.self:Await替换为await
# 12.self:AwaitAll替换为await Promise.all()
# 13.如果遇到潜在的外部模块，在输出的TypeScript代码顶部输出对应的import语句
# 14.字符串用单引号
# 15.使用===和!==