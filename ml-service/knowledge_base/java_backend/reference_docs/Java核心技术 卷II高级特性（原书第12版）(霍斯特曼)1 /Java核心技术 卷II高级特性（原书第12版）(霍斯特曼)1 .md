**ORACLE** PRESS

![](_page_0_Picture_1.jpeg)

Java核心技术系列

涵盖Java 17 新特性

Core Java, Volume II: Advanced Features, Twelfth Edition

# 引 名 径 核 心 技术

卷II 高级特性

(原书第12版)

[美]凯·S. 霍斯特曼(Cay S. Horstmann)著 陈昊鹏译

ORACLE

![](_page_0_Picture_10.jpeg)

Core Java, Volume II: Advanced Features, Twelfth Edition

# JaVa 核心技术

卷II 高级特性 (原书第12版)

[美] 凯·S. 霍斯特曼 (Cay S. Horstmann) 著 陈昊鹏 译

![](_page_1_Picture_5.jpeg)

# 图书在版编目 (CIP) 数据

Java 核心技术: 原书第 12 版. 卷 Ⅱ, 高级特性 / (美) 凯·S. 霍斯特曼 (Cay S. Horstmann) 著; 陈昊鹏译. -- 北京: 机械工业出版社, 2023.1 (2023.5 重印) (Java 核心技术系列)

书名原文: Core Java, Volume II: Advanced Features, 12e ISBN 978-7-111-71974-8

I. ① J··· II. ①凯··· ②陈··· III. ① JAVA 语言 - 程序设计 IV. ① TP312.8

中国版本图书馆 CIP 数据核字(2022)第 207607号

北京市版权局著作权合同登记 图字: 01-2022-3136号。

Authorized translation from the English language edition, entitled *Core Java, Volume II: Advanced Features, Twelfth Edition*, ISBN: 978-0-13-787107-0, by Cay S. Horstmann, published by Pearson Education, Inc., Copyright © 2022 Pearson Education Inc., Portions copyright © 1996-2013 Oracle and/or its affiliates.

All rights reserved. No part of this book may be reproduced or transmitted in any form or by any means, electronic or mechanical, including photocopying, recording or by any information storage retrieval system, without permission from Pearson Education, Inc.

Chinese simplified language edition published by China Machine Press, Copyright © 2022.

本书中文简体字版由 Pearson Education (培生教育出版集团)授权机械工业出版社在中国大陆地区(不包括香港、澳门特别行政区及台湾地区)独家出版发行。未经出版者书面许可,不得以任何方式抄袭、复制或节录本书中的任何部分。

本书封底贴有 Pearson Education (培生教育出版集团) 激光防伪标签, 无标签者不得销售。

# Java 核心技术 卷Ⅱ 高级特性 (原书第12版)

出版发行: 机械工业出版社(北京市西城区百万庄大街 22号 邮政编码: 100037)

策划编辑: 王 颖

责任校对:梁园张征

版 次: 2023年5月第1版第2次印刷

开 本: 186mm×240mm 1/16

书 号: ISBN 978-7-111-71974-8

客服电话: (010) 88361066

(010) 68326294

责任编辑: 王 颖

责任印制: 常天培

印刷: 固安县铭成印刷有限公司

印 张: 43.5

定 价: 149.00元

版权所有·侵权必究 封底无防伪标均为盗版

# 译者序

《Java 核心技术 卷Ⅱ: 高级特性》的第 12 版问世了,它针对最新的长期支持版本——Java 17 进行了更新,并删除了过时的内容。这一版与第 11 版相比,各个章节的安排没有发生重大调整,主要关注了 Java 17 带来的新特性,这也反映了 Java 语言近期平稳发展的特点。近几年,Python 语言在数据科学和机器学习领域大放异彩,使得人们倍加关注 Java 语言的发展方向。从目前的发展趋势来看,我们仍相信,Java 完备的语言特性和丰富的生态圈会使它在今后很长的一段时间内都还是一种无法被替代的编程语言。

第 12 版针对 Java 17 的新特性进行了内容更新和扩展,经验丰富的程序员可以将其作为 Java 编程的指导手册,初学者也可以将其中大量的示例作为编写自己程序的蓝本 $^{\ominus}$ 。

第 12 版的中文版是在之前版本的基础上完成的。在翻译本书的过程中,译者不但对更新的内容进行了翻译,还着力对第 11 版中存在的错误和不符合中文表达习惯的地方进行了修正,力求以准确和流畅的语言重现英文版的内容和韵味,希望读者在阅读本书时能够感受到 Java 的魅力和作者的风格。

我们有理由相信, Java 语言在万物互联的时代还会继续成为编程语言中的中流砥柱之一, 并且会在与其他优秀编程语言不断竞争的过程中互相学习和进步,展示出更强大的能力和 韧性。

陈昊鹏

<sup>○</sup> 本书提供作者亲授官方讲解课程视频(中文配音+中文字幕), B 站搜索 "Java 核心技术站"免费观看。一编辑注

# *刖*

# *致读者*

*本书是完整更新到Java <sup>17</sup> 《Java核心技术》 <sup>12</sup> <sup>卷</sup>II。<sup>卷</sup>I<sup>主</sup> <sup>介</sup> <sup>了</sup> Java 一些关 性 本卷主 介 人员 专业 件开发时 了 主 。因 <sup>此</sup> 与卷I和之前 本一样 我们仍将本书 定位于 Java技术 <sup>实</sup> 开发 人员。*

*写任何一本书 免会有一些 或不准 地方。我们 常乐意听到 意 。 当然 我们更希望对 同 报告只出 一次。为此 我们创建了一个关于FAQ、bug修 正以及应急方案 http:// horstmann.com/corejavao你可以在bug报告 末尾处 <sup>励</sup> 以前 报告 添加bug报告 以此来发布bug和 并 出建 以便我们提 本 书未来 本的质量。*

# *内容提*

*本书中的章节大 分是 互独立的。你可以 己最感兴 主 并可以按照任意 序 些 。*

*在 1 <sup>中</sup> 你将学习Java <sup>流</sup> 它带来了 <sup>代</sup> <sup>格</sup> 数据处 机制 即只 指定想 果 无 描 应 如何 得 果。 使得流可以专注于优化 对 于优化并发 来 显得 别有利。*

*2 <sup>主</sup> <sup>是</sup> <sup>人</sup>/ 出处 。在Java<sup>中</sup> 所有I/O <sup>是</sup> <sup>人</sup>/ 出流来处 。 些流 不 与 1 些流混淆了 使你可以按照 一 方式来处 与各 数据源之 信 例如文件、 接或内存块。我们对各 入器和写出器 了 它 们使得对Unicode 处 变得很容易。我们 展 了使 对 序列化机制使保存和加 对 变 得容易 方便 方法 以及对 序列化机制 后 原 。然后 我们 了正则 式以及如 何操作文件与 径。 包含了最新 Java 本中引人 广受欢 改 和优化。*

*3 介 XML,展 怎样 析XML文件、怎样 成XML以及怎样使 XSL 换。在一个实 例中 我们将展 怎样在XML中指定Swing 体 布局。我们 了 XPathAPI,它使得"在XML 大海中捞 "变得更加容易。*

*4 介绍网络API。Java使复杂 工作变得很容易实 。我们将介 怎样 接到服务器 怎样实 你 己 服务器 以及怎样创建HTTP 接。 了新 HTTP客户 。*

第5章介绍数据库编程,重点讲解 JDBC,即 Java 数据库连接 API,这是用于将 Java 程序与关系数据库进行连接的 API。我们将介绍怎样通过使用 JDBC API 的核心子集,编写能够处理实际的数据库日常操作事务的实用程序。(如果要完整介绍 JDBC API 的功能,可能需要编写一本像本书一样厚的书才行。)

Java 对于处理日期和时间的类库做出过两次设计,而在 Java 8 中做出的第三次设计则极富魅力。在第6章中,你将学习如何使用新的日期和时间库来处理日历和时区的复杂性。

第7章讨论一个我们认为其重要性将会不断提升的特性——国际化。Java 编程语言是少数几种一开始就被设计为可以处理 Unicode 的语言之一,不过 Java 平台的国际化支持则走得更远。因此,你可以对 Java 应用程序进行国际化,使其不仅可以跨平台,而且还可以跨国界。例如,我们会展示怎样编写一个使用英语、德语和汉语的退休金计算器。

第8章讨论三种处理代码的技术。脚本机制和编译器 API 允许程序去调用使用诸如 JavaScript 或 Groovy 之类的脚本语言编写的代码,并且允许程序去编译 Java 代码。可以使用注解向 Java 程序中添加任意信息(有时称为元数据)。我们将展示注解处理器怎样在源码级别或者类文件级别上收集注解,以及怎样运用注解来影响运行时的类行为。注解只有在工具的支持下才有用,因此,我们希望这些讨论能够帮助你根据需要选择有用的注解处理工具。

第9章讲解从 Java 9 开始引入的 Java 平台模块系统,以促进 Java 平台和核心类库的有序演化。这个模块系统提供了对包的封装和用于描述模块需求的机制。你将学习模块的属性,以便决定是否要在自己的应用程序中使用它们。即使你决定不使用,也需要了解这些新规则,这样你才能和 Java 平台以及其他模块化的类库交互。

第 10 章介绍 Java 安全类库中的 Java 安全模型、用户认证和加密功能。你将学习有关消息、代码签名、授权和认证以及加密等重要特性。最后,我们以使用 AES 和 RSA 加密算法的示例进行总结。

第 11 章讨论没有纳入卷 I 的所有 Swing 知识,尤其是重要但很复杂的树构件和表格构件。我们还会介绍 Java 2D API,你可以用它来创建写实的图形和特殊的效果。当然,如今已经没有多少程序员需要编写 Swing 用户界面了,因此我们会将注意力放到在服务器端生成图像的实用特性上。

第12章介绍本地方法,这个功能支持你调用为微软 Windows API 这样的特定机器而编写的各种方法。很显然,这种特性具有争议:使用本地方法,那么 Java 平台的跨平台特性将会随之消失。但是,每个为特定平台编写 Java 应用程序的专业开发人员都需要了解这些技术,因为有时,当你与不支持 Java 平台的设备或服务进行交互时,为了你的目标平台,你可能需要求助于操作系统 API。我们将通过展示如何从某个 Java 程序访问 Windows 注册表 API来阐明这一点。

所有章节都按照最新版本的 Java 进行了修订,过时的材料都删除了,对 Java 17 的新 API 都详细地进行了讨论。

## *定*

*我们使用等宽字体表示计算机代 格式在众多 机书 中极为常 。各 图 标 含义如下*

*0 <sup>注</sup> <sup>引</sup> 注意 地方。*

*场<sup>提</sup> 有用的提 。*

*0 <sup>告</sup> 关于 或危 情况 告信息。*

*9 C++<sup>注</sup> 本书中有 多这类提 <sup>于</sup> Java <sup>序</sup> <sup>和</sup>C++语言之间的 不同。如果你对 分不感兴 可以跳过。*

*Java平台 备有大 库或 应 序 接口 API 。当 一次使 某个API 时 我们在每一 末尾 添加了 描 。 些描 可 有点不太 但是比官方在 API文档更具指导性。 、接口或方法名后 数字是JDK 本 在 本中才 引人了 应的特性。*

# *@应 序 接口*

*本书 例代 以 序清单 形式列举出来 例如*

# *序清单 0-1 ScriptTest.java*

*可以从网站http://horstmann.com/corejava下 例代 。*

# 致 谢

写一本书需要投入大量的精力,升级一本书也并不像想象的那样轻松,尤其是 Java 技术一直在持续不断地更新。出版一本书会让很多人耗费很多心血,在此衷心地感谢《 Java 核心技术》小组的每一位成员。

Pearson 公司的许多人提供了非常有价值的帮助,却甘愿做幕后英雄。在此,我希望大家都能够知道我对他们努力的感恩。与以往一样,我要真诚地感谢我的编辑 Greg Doench,从本书的写作到出版他一直在给予我们指导,同时感谢那些不知其姓名的为本书做出贡献的幕后人士。非常感谢 Julie Nahil 在图书制作方面给予的支持,感谢 Dmitry Kirsanov 和 Alina Kirsanova 完成手稿的编辑与排版工作。

感谢早期版本的许多读者,他们指出了许多令人尴尬的错误并给出了许多具有建设性的修改意见。我还要特别感谢本书优秀的审校小组,他们仔细地审阅我的手稿,使本书减少了许多错误。

这一版及以前版本是由以下人员评审的: Chuck Allison (犹他谷大学)、Lance Anderson (Oracle), Gail Anderson (Anderson Software Group), Paul Anderson (Anderson Software Group), Alec Beaton (IBM), Cliff Berg, Andrew Binstock (Oracle), Joshua Bloch, David Brown, Corky Cartwright, Frank Cohen (PushToTest), Chris Crane (devXsolution), Nicholas J. De Lillo 博士 (曼哈顿学院)、Rakesh Dhoopar (Oracle)、Robert Evans (资深教师, 约翰斯・霍 普金斯大学应用物理实验室)、David Geary (Clarity Training)、Jim Gish (Oracle)、Brian Goetz (Oracle), Angela Gordon, Dan Gordon (Electric Cloud), Rob Gordon, John Gray (哈特福德大学)、Cameron Gregory (olabs.com)、Steve Haines、Marty Hall (coreservlets. com, Inc.)、Vincent Hardy (Adobe Systems)、Dan Harkey (圣何塞州立大学)、William Higgins (IBM), Marc Hoffmann (mtrail), Vladimir Ivanovic (PointBase), Jerry Jackson (CA Technologies), Heinz Kabutz (Java Specialists), Stepan V. Kalinin (I-Teco/Servionica LTD), Tim Kimmet (Walmart), Chris Laffra, Charlie Lai (Apple), Angelika Langer, Jeff Langr (Langr Software Solutions)、Doug Langston、Hang Lau (麦吉尔大学)、Mark Lawrence、Doug Lea (纽约州立大学奥斯威戈分校)、Gregory Longshore、Bob Lynch (Lynch Associates)、Philip Milne (顾问)、Mark Morrissey (俄勒冈研究生院)、Mahesh Neelakanta (佛罗里达大西洋大 学)、José Paumard (Oracle)、Hao Pham、Paul Philion、Blake Ragsdell、Ylber Ramadani (瑞 尔森大学)、Stuart Reges(亚利桑那大学)、Simon Ritter(Azul Systems)、Rich Rosen(Interactive Data Corporation)、Peter Sanders (法国尼斯ESSI大学)、Paul Sanghera 博士 (圣何塞州 立大学和布鲁克斯学院)、Paul Sevinc (Teamup AG)、Devang Shah (Sun Microsystems)、 Yoshiki Shiabata、Richard Slywczak (NASA/Glenn 研究中心)、Bradley A. Smith、Steven Stelling (Oracle)、Christopher Taylor、Luke Taylor (Valtech)、George Thiruvathukal、Kim Topley (StreamingEdge)、Janet Traub、Paul Tyma (顾问)、Christian Ullenboom、Peter van der Linden、Burt Walsh、JoeWang (Oracle)、Dan Xu (Oracle) 和 John Zavgren (Oracle)。

Cay S. Horstmann 2022 年 1 月于德国柏林

# 目 录

| 译者序                                       | 2.1.3 组合输入/输出流过滤器50                   |
|-------------------------------------------|---------------------------------------|
| 前言                                        | 2.1.4 文本输入与输出53                       |
| 致谢                                        | 2.1.5 如何写出文本输出53                      |
|                                           | 2.1.6 如何读入文本输入55                      |
| 第 1 章 流·································· | 2.1.7 以文本格式存储对象56                     |
| 1.1 从迭代到流的操作                              | 2.1.8 字符编码方式59                        |
| 1.2 流的创建3                                 | 2.2 读写二进制数据61                         |
| 1.3 filter、map 和 flatMap 方法8              | 2.2.1 DataInput 和 DataOutput 接口…61    |
| 1.4 抽取子流和组合流10                            | 2.2.2 随机访问文件63                        |
| 1.5 其他的流转换11                              | 2.2.3 ZIP 文档···················67     |
| 1.6 简单约简12                                | 2.3 对象输入/输出流与序列化70                    |
| 1.7 Optional 类型······13                   | 2.3.1 保存和加载序列化对象70                    |
| 1.7.1 获取 Optional 值······13               | 2.3.2 理解对象序列化的文件格式…74                 |
| 1.7.2 消费 Optional 值······14               | 2.3.3 修改默认的序列化机制79                    |
| 1.7.3 管道化 Optional 值······15              | 2.3.4 readResolve 和 writeReplace 方法82 |
| 1.7.4 不适合使用 Optional 值的方式···15            | 2.3.5 版本管理84                          |
| 1.7.5 创建 Optional 值······17               | 2.3.6 为克隆使用序列化86                      |
| 1.7.6 用 flatMap 构建 Optional 值的            | 2.3.7 反序列化和安全88                       |
| 函数17                                      | 2.4 操作文件90                            |
| 1.7.7 将 Optional 转换为流······18             | 2.4.1 Path 90                         |
| 1.8 收集结果20                                | 2.4.2 读写文件92                          |
| 1.9 收集到映射表中24                             | 2.4.3 创建文件和目录93                       |
| 1.10 群组和分区27                              | 2.4.4 复制、移动和删除文件94                    |
| 1.11 下游收集器28                              | 2.4.5 获取文件信息96                        |
| 1.12 约简操作33                               | 2.4.6 访问目录中的项97                       |
| 1.13 基本类型流34                              | 2.4.7 使用目录流98                         |
| 1.14 并行流39                                | 2.4.8 ZIP 文件系统······101               |
| 第2章 输入与输出 3                               | 2.5 内存映射文件102                         |
| 2.1 输入/输出流                                | 2.5.1 内存映射文件的性能102                    |
| 2.1.1 读写字节                                | 2.5.2 缓冲区数据结构108                      |
| 2.1.2 完整的流家族                              | 2.6 文件加锁机制110                         |

| 2.7 正则表达式112                | 4.2.3 半关闭          | 196                  |
|-----------------------------|--------------------|----------------------|
| 2.7.1 正则表达式语法112            | 4.2.4 可中断套持        | 妾字197                |
| 2.7.2 匹配整个字符串115            | 4.3 获取 Web 数据      | 203                  |
| 2.7.3 找出字符串中的所有匹配116        | 4.3.1 URL 和 U.     | RI203                |
| 2.7.4 群组117                 | 4.3.2 使用 URLCon    | nection 获取信息·····205 |
| 2.7.5 用分隔符来分割119            | 4.3.3 提交表单数        | 效据211                |
| 2.7.6 替换匹配120               | 4.4 HTTP 客户端··     | 219                  |
| 2.7.7 标志120                 | 4.4.1 HttpClient   | 类219                 |
| 第3章 XML······124            | 4.4.2 HttpRequest  | 类和体发布器220            |
| 3.1 XML 概述······124         | 4.4.3 HttpResponse | 接口和体处理器…220          |
| 3.2 XML 文档的结构 ······126     | 4.4.4 异步处理         | 221                  |
| 3.3 解析 XML 文档······128      | 4.5 发送 E-mail····  | 226                  |
| 3.4 验证 XML 文档······137      | 第5章 数据库编程          | ₹229                 |
| 3.4.1 文档类型定义137             |                    | 229                  |
| 3.4.2 XML Schema144         |                    | <b>起序类型230</b>       |
| 3.4.3 一个实践示例146             |                    | 型用法231               |
| 3.5 使用 XPath 来定位信息152       |                    | 言231                 |
| 3.6 使用命名空间156               |                    | 236                  |
| 3.7 流机制解析器158               |                    | L236                 |
| 3.7.1 使用 SAX 解析器158         |                    | JAR 文件······237      |
| 3.7.2 使用 StAX 解析器163        |                    | 车237                 |
| 3.8 生成 XML 文档······166      |                    | 器类·······238         |
| 3.8.1 不带命名空间的文档166          |                    | 居库238                |
| 3.8.2 带命名空间的文档167           |                    | 句241                 |
| 3.8.3 写出文档167               |                    | 语句······ <i>241</i>  |
| 3.8.4 使用 StAX 写出 XML 文档…169 |                    | 语句和结果集244            |
| 3.8.5 示例: 生成 SVG 文件174      |                    |                      |
| 3.9 XSL 转换······ <i>175</i> |                    | 异常244                |
| 第 4 章 网络184                 |                    | 车······246           |
| 4.1 连接到服务器184               |                    | 250                  |
| 4.1.1 使用 telnet ·······184  |                    | 250                  |
| 4.1.2 用 Java 连接到服务器186      |                    | 256                  |
| 4.1.3 套接字超时188              |                    | 257                  |
| 4.1.4 因特网地址189              | - 47 1 111         | 259                  |
| 4.2 实现服务器190                |                    | 生成的键······260        |
| 4.2.1 服务器套接字190             | 5.6 可滚动和可更         | 新的结果集260             |
| 4.2.2 为多个客户端服务193           | 5.6.1 可滚动的         | 吉果集260               |

| 5.6.2 可更新的结果集262                  | 7.6.2 行结束符328                  |
|-----------------------------------|--------------------------------|
| 5.7 行集265                         | 7.6.3 控制台328                   |
| 5.7.1 构建行集266                     | 7.6.4 日志文件 329                 |
| 5.7.2 被缓存的行集266                   | 7.6.5 UTF-8 字节顺序标志 ·······329  |
| 5.8 元数据269                        | 7.6.6 源文件的字符编码329              |
| 5.9 事务278                         | 7.7 资源包330                     |
| 5.9.1 用 JDBC 对事务编程 ·······278     | 7.7.1 定位资源包330                 |
| 5.9.2 保存点279                      | 7.7.2 属性文件331                  |
| 5.9.3 批量更新279                     | 7.7.3 包类332                    |
| 5.9.4 高级 SQL 类型······281          | 7.8 一个完整的例子333                 |
| 5.10 Web 与企业应用中的连接管理…·282         | 第8章 脚本、编译与注解处理348              |
| 第6章 日期和时间 API284                  | 8.1 Java 平台的脚本机制 ·······348    |
| 6.1 时间线284                        | 8.1.1 获取脚本引擎348                |
| 6.2 本地日期288                       | 8.1.2 脚本计算与绑定 349              |
| 6.3 日期调整器292                      | 8.1.3 重定向输入和输出351              |
| 6.4 本地时间293                       | 8.1.4 调用脚本的函数和方法352            |
| 6.5 时区时间294                       | 8.1.5 编译脚本353                  |
| 6.6 格式化和解析298                     | 8.1.6 示例: 用脚本处理 GUI 事件 … 354   |
| 6.7 与遗留代码的互操作302                  | 8.2 编译器 API·······358          |
| 第7章 国际化304                        | 8.2.1 调用编译器 ······358          |
| 7.1 locale                        | 8.2.2 发起编译任务359                |
| 7.1.1 为什么需要 locale ···········304 | 8.2.3 捕获诊断消息359                |
| 7.1.2 指定 locale305                | 8.2.4 从内存中读取源文件 360            |
| 7.1.3 默认 locale                   | 8.2.5 将字节码写出到内存中360            |
| 7.1.4 显示名字······308               | 8.2.6 示例: 动态 Java 代码生成362      |
| 7.2 数字格式309                       | 8.3 使用注解367                    |
| 7.2.1 格式化数字值310                   | 8.3.1 注解简介368                  |
| 7.2.2 DecimalFormat 类313          | 8.3.2 示例: 注解事件处理器369           |
| 7.2.3 货币315                       | 8.4 注解语法 373                   |
| 7.3 日期和时间316                      | 8.4.1 注解接口373                  |
| 7.4 排序和规范化319                     | 8.4.2 注解375                    |
| 7.5 消息格式化324                      | 8.4.3 注解各类声明376                |
| 7.5.1 格式化数字和日期324                 | 8.4.4 注解类型用法377                |
| 7.5.2 选择格式325                     | 8.4.5 注解 this······ <i>378</i> |
| 7.6 文本输入和输出327                    | 8.5 标准注解379                    |
| 7.6.1 文本文件327                     | 8.5.1 用于编译的注解380               |

| 8.5.2 元注解381                    | 10.3.3 校验签名445                 |
|---------------------------------|--------------------------------|
| 8.6 源码级注解处理383                  | 10.3.4 认证问题447                 |
| 8.6.1 注解处理器383                  | 10.3.5 证书签名                    |
| 8.6.2 语言模型 API······384         | 10.3.6 证书请求                    |
| 8.6.3 使用注解来生成源码384              | 10.3.7 代码签名450                 |
| 8.7 字节码工程387                    | 10.4 加密452                     |
| 8.7.1 修改类文件387                  | 10.4.1 对称密码                    |
| 8.7.2 在加载时修改字节码392              | 10.4.2 密钥生成454                 |
| 第 9 章 Java 平台模块系统 ······395     | 10.4.3 密码流                     |
| 9.1 模块的概念395                    | 10.4.4 公共密钥密码459               |
| 9.2 对模块命名396                    | 第 11 章 高级 Swing 和图形化编程 ··· 463 |
| 9.3 模块化的 "Hello, World!" 程序…397 | 11.1 表格463                     |
| 9.4 对模块的需求 398                  | 11.1.1 一个简单表格463               |
| 9.5 导出包······400                | 11.1.2 表格模型466                 |
| 9.6 模块化的 JAR·······403          | 11.1.3 对行和列的操作                 |
| 9.7 模块和反射式访问404                 | 11.1.4 单元格的绘制和编辑483            |
| 9.8 自动模块406                     | 11.2 树                         |
| 9.9 不具名模块408                    | 11.2.1 简单的树494                 |
| 9.10 用于迁移的命令行标识                 | 11.2.2 节点枚举506                 |
| 9.11 传递的需求和静态的需求410             | 11.2.3 绘制节点508                 |
| 9.12 限定导出和开放411                 | 11.2.4 监听树事件510                |
| 9.13 服务加载412                    | 11.2.5 定制树模型516                |
| 9.14 操作模块的工具414                 | 11.3 高级 AWT······524           |
| 第 10 章 安全                       | 11.3.1 绘图操作流程524               |
| 10.1 类加载器417                    | 11.3.2 形状526                   |
| 10.1.1 类加载过程418                 | 11.3.3 区域540                   |
| 10.1.2 类加载器的层次结构418             | 11.3.4 笔画541                   |
| 10.1.3 将类加载器用作命名空间…420          | 11.3.5 着色548                   |
| 10.1.4 编写你自己的类加载器421            | 11.3.6 坐标变换549                 |
| 10.1.5 字节码校验426                 | 11.3.7 剪切554                   |
| 10.2 用户认证429                    | 11.3.8 透明与组合555                |
| 10.2.1 JAAS 框架······429         | 11.4 像素图563                    |
| 10.2.2 JAAS 登录模块······432       | 11.4.1 图像的读取器和写入器563           |
| 10.3 数字签名440                    | 11.4.2 图像处理571                 |
| 10.3.1 消息摘要440                  | 11.5 打印584                     |
| 10.3.2 消息签名443                  | 11.5.1 图形打印584                 |

| 11.5.2 打印多页文件592                    | 12.6.2 静态方法633                    |
|-------------------------------------|-----------------------------------|
| 11.5.3 打印服务程序600                    | 12.6.3 构造器634                     |
| 11.5.4 流打印服务程序602                   | 12.6.4 另一种方法调用634                 |
| 11.5.5 打印属性605                      | 12.7 访问数组元素636                    |
| 第 12 章 本地方法612                      | 12.8 错误处理639                      |
| 12.1 从 Java 程序中调用 C 函数613           | 12.9 使用调用 API·················643 |
| 12.2 数值参数与返回值617                    | 12.10 完整的示例: 访问 Windows           |
| 12.3 字符串参数619                       | 注册表648                            |
| 12.4 访问域624                         |                                   |
| 12.4.1 访问实例域624                     | 12.10.1 Windows 注册表概述648          |
| 12.4.2 访问静态域628                     | 12.10.2 访问注册表的 Java 平台接口…649      |
| 12.5 编码签名628                        | 12.10.3 以本地方法实现注册表                |
| 12.6 调用 Java 方法·················630 | 访问函数650                           |
| 12.6.1 实例方法630                      | 12.11 外部函数: 展望未来662               |

# 第1章 流

- ▲ 从迭代到流的操作
- ▲ 流的创建
- ▲ filter、map 和 flatMap 方法
- ▲ 抽取子流和组合流
- ▲ 其他的流转换
- ▲ 简单约简
- ▲ Optional 类型

- ▲ 收集结果
- ▲ 收集到映射表中
- ▲ 群组和分区
- ▲ 下游收集器
- ▲ 约简操作
- ▲ 基本类型流
- ▲ 并行流

与集合相比,流提供了一种可以让我们在更高的概念级别上指定计算任务的数据视图。通过使用流,我们可以指明想要完成什么任务,而不是指明如何去实现它。我们将操作的调度留给具体实现去解决。例如,假设我们想要计算某个属性的平均值,那么我们就可以指定数据源和该属性,然后,流库就可以对计算进行优化,例如,使用多线程来计算总和与个数,并将结果组合起来计算最终的平均值。

在本章中, 你将会学习如何使用 Java 的流库, 它是在 Java 8 中引入的, 用来以"做什么而非怎么做"的方式处理集合。

# 1.1 从迭代到流的操作

在处理集合时,我们通常会迭代遍历它的元素,并在每个元素上执行某项操作。例如, 假设我们想要对某本书中的所有长单词进行计数。首先,将所有单词放到一个列表中:

```
var contents = Files.readString(Path.of("alice.txt")); // Read file into string
List<String> words = List.of(contents.split("\\PL+"));
    // Split into words; nonletters are delimiters

现在, 我们可以迭代它了:\nint count = 0;
for (String w : words)
{
    if (w.length() > 12) count++;
}

在使用流时, 相同的操作看起来像下面这样:
long count = words.stream()
    .filter(w -> w.length() > 12)
    .count();
```

现在我们不必扫描整个代码去查找过滤和计数操作,方法名就可以直接告诉我们其代码 意欲何为。而且,循环需要非常详细地指定操作的顺序,而流却能够以其想要的任何方式来 调度这些操作,只要结果是正确的即可。

仅将 stream 修改为 parallelStream 就可以让流库以并行方式来执行过滤和计数。

```
long count = words.parallelStream()
   .filter(w -> w.length() > 12)
   .count();
```

流遵循了"做什么而非怎么做"的原则。在流的示例中,我们描述了需要做什么:获取 长单词,并对它们计数。我们没有指定该操作应该以什么顺序或者在哪个线程中执行。相比 之下,本节开头处的循环要确切地指定计算应该如何工作,因此也就丧失了进行优化的机会。

流表面上看起来和集合很类似,都可以让我们转换和获取数据。但是,它们之间存在着显著的差异:

- 1. 流并不存储其元素。这些元素可能存储在底层的集合中,或者是按需生成的。
- 2. 流的操作不会修改其数据源。例如, filter 方法不会从流中移除元素, 而是会生成一个新的流, 其中不包含被过滤掉的元素。
- 3. 流的操作是尽可能惰性执行的。这意味着直至需要其结果时,操作才会执行。例如,如果我们只想查找前 5 个长单词而不是所有长单词,那么 filter 方法就会在匹配到第 5 个单词后停止过滤。因此,我们甚至可以操作无限流。

我们再来看看这个示例。stream 和 parallelStream 方法会产生一个用于 words 列表的流。filter 方法会返回另一个流,其中只包含长度大于 12 的单词。count 方法会将这个流约简为一个结果。

这个工作流是操作流时的典型流程。我们建立了一个包含三个阶段的操作管道:

- 1. 创建一个流。
- 2. 指定将初始流转换为其他流的中间操作,可能包含多个步骤。
- 3. 应用终止操作,从而产生结果。这个操作会强制执行之前的惰性操作。从此之后,这个流就再也不能用了。

在程序清单 1-1 的示例中,流是用 stream 或 parallelStream 方法创建的。filter 方法对 其进行转换,而 count 方法是终止操作。

# 程序清单 1-1 streams/CountLongWords.java

```
package streams;
\nimport java.io.*;\nimport java.nio.file.*;\nimport java.util.*;

/**
 * @version 1.02 2019-08-28
 * @author Cay Horstmann
 */
public class CountLongWords
{
```

```
public static void main(String[] args) throws IOException
14
         var contents = Files.readString(
15
            Path.of("../gutenberg/alice30.txt"));
16
         List<String> words = List.of(contents.split("\\PL+"));
17
18
         long count = \theta;
19
         for (String w : words)
28
21
            if (w.length() > 12) count++;
22
23
         System.out.println(count);
25
         count = words.stream().filter(w -> w.length() > 12).count();
26
         System.out.println(count);
27
28
         count = words.parallelStream().filter(w -> w.length() > 12).count();
29
30
         System.out.println(count);
31
32 }
```

在下一节中, 你将会看到如何创建流; 后续的三节将讨论流的转换; 再后面的五节将讨论终止操作。

#### API java.util.stream.Stream<T>

- Stream<T> filter(Predicate<? super T> p) 产生一个流,其中包含当前流中满足 p 的所有元素。
- long count()产生当前流中元素的数量。这是一个终止操作。

# API java.util.Collection<E>

- default Stream<E> stream()
- default Stream
   parallelStream()
   产生当前集合中所有元素的顺序流或并行流。

# 1.2 流的创建

你已经看到了可以用 Collection 接口的 stream 方法将任何集合转换为一个流。如果你有一个数组,那么可以转而使用静态的 Stream.of 方法。

```
Stream<String> words = Stream.of(contents.split("\\PL+"));
// split returns a String[] array
```

of 方法具有可变长参数, 因此我们可以构建具有任意数量引元的流:

```
Stream<String> song = Stream.of("gently", "down", "the", "stream");
```

使用 Array. stream(array, from, to) 可以用数组中的一部分元素来创建一个流。

4

为了创建不包含任何元素的流,可以使用静态的 Stream.empty 方法:

Stream<String> silence = Stream.empty();
 // Generic type <String> is inferred; same as Stream.<String>empty()

Stream 接口有两个用于创建无限流的静态方法。generate 方法会接受一个不包含任何引元的函数(或者从技术上讲,是一个 Supplier<T> 接口的对象)。无论何时,只要需要一个流类型的值,该函数就会被调用以产生一个这样的值。我们可以像下面这样获得一个常量值的流:

Stream<String> echos = Stream.generate(() -> "Echo");

或者像下面这样获取一个随机数的流:

Stream<Double> randoms = Stream.generate(Math::random);

如果要产生像 0 1 2 3 ··· 这样的序列,可以使用 iterate 方法。它会接受一个"种子"值,以及一个函数 (从技术上讲,是一个 UnaryOperator<T>),并且会反复地将该函数应用到之前的结果上。例如,

Stream<BigInteger> integers

该序列中的第一个元素是种子 BigInteger.ZERO, 第二个元素是 f(seed), 即 1(作为大整数), 下一个元素是 f(f(seed)), 即 2, 后续以此类推。

如果要产生一个有限序列,则需要添加一个谓词来描述迭代应该如何结束:

var limit = new BigInteger("10000000");
Stream<BigInteger> integers

只要该谓词拒绝了某个迭代生成的值,这个流即结束。

最后, Stream.ofNullable 方法会用一个对象来创建一个非常短的流。如果该对象为 null, 那么这个流的长度就为 0; 否则,这个流的长度为 1,即只包含该对象。这个方法与 flatMap 相结合时最有用,可以查看 1.7.7 节中的示例。

i 注释: Java API 中有大量方法都可以产生流。例如, String 类有一个 lines 方法, 它 会产生一个由字符串中所有的行构成的流:

Stream<String> greetings = "Hello\nGuten Tag\nBonjour".lines()

Pattern 类有一个 splitAsStream 方法,它会按照某个正则表达式来分割一个 CharSequence 对象。可以使用下面的语句来将一个字符串分割为一个个的单词:

Stream<String> words = Pattern.compile("\\PL+").splitAsStream(contents);

Scanner.tokens 方法会产生一个扫描器的符号流。另一种从字符串中获取单词流的方式是:

Stream<String> words = new Scanner(contents).tokens();

静态的 Files, lines 方法会返回一个包含了文件中所有行的 Stream:

```
try (Stream<String> lines = Files.lines(path))
{
    Process lines
}
```

要想查看本节介绍的流中的内容,可以使用 toList 方法,它会将流中的元素收集到一个列表中。就像 count 一样,toList 也是一个终止操作。如果流是无限的,那么首先要用 limit 方法截断它:

System.out.println(Stream.generate(Math::random).limit(10).toList());

直 注释:如果我们持有的 Iterable 对象不是集合,那么可以通过下面的调用将其转换为一个流:

StreamSupport.stream(iterable.spliterator(), false);

如果我们持有的是 Iterator 对象,并且希望得到一个由它的结果构成的流,那么可以使用下面的语句:

StreamSupport.stream(Spliterators.spliteratorUnknownSize(
 iterator, Spliterator.ORDERED), false);

◆ 警告: 至关重要的是,在执行流的操作时,我们并没有修改流背后的集合。记住,流并没有收集其数据,数据一直存储在单独的集合中。如果修改了该集合,那么流操作的结果就会变成未定义的。JDK 文档称这种要求为不干涉性。

准确地讲,因为中间的流操作是惰性的,所以在终止操作得以执行时,集合有可能已经发生了变化。例如,尽管我们不推荐下面这段代码,但是它仍旧可以工作:

```
List<String> wordList = . . .;
Stream<String> words = wordList.stream();
wordList.add("END");
long n = words.distinct().count();
```

但是下面的代码是错误的:

```
Stream<String> words = wordList.stream();
words.forEach(s -> {} if (s.length() < 12) wordList.remove(s); {});
   // ERROR--interference</pre>
```

程序清单 1-2 中的示例程序展示了创建流的各种方式。

#### 程序清单 1-2 streams/CreatingStreams.java

```
package streams;
\nimport java.io.*;\nimport java.math.*;\nimport java.nio.file.*;\nimport java.util.*;\nimport java.util.regex.Pattern;\nimport java.util.stream.*;

/**

* @version 1.03 2021-09-06
```

```
* @author Cay Horstmann
12
   */
13
   public class CreatingStreams
14
15
      public static <T> void show(String title, Stream<T> stream)
16
17
         final int SIZE = 10;
18
         List<T> firstElements = stream
19
20
             .limit(SIZE + 1)
             .toList();
21
         System.out.print(title + ": ");
22
         for (int i = 0; i < firstElements.size(); i++)
23
24
             if (i > 0) System.out.print(", ");
25
             if (i < SIZE) System.out.print(firstElements.get(i));</pre>
26
             else System.out.print("...");
27
28
         System.out.println();
29
30
31
      public static void main(String[] args) throws IOException
32
33
          Path path = Path.of("../gutenberg/alice30.txt");
34
35
         var contents = Files.readString(path);
36
          Stream<String> words = Stream.of(contents.split("\\PL+"));
37
          show("words", words);
38
          Stream<String> song = Stream.of("gently", "down", "the", "stream");
30
          show("song", song);
48
          Stream<String> silence = Stream.empty();
41
          show("silence", silence);
42
43
          Stream<String> echos = Stream.generate(() -> "Echo");
44
          show("echos", echos);
45
46
          Stream<Double> randoms = Stream.generate(Math::random);
47
          show("randoms", randoms);
48
49
          Stream<BigInteger> integers = Stream.iterate(BigInteger.ONE,
58
             n -> n.add(BigInteger.ONE));
51
          show("integers", integers);
52
53
          Stream<String> greetings = "Hello\nGuten Tag\nBonjour".lines();
54
          show("greetings", greetings);
55
56
          Stream<String> wordsAnotherWay = Pattern.compile("\\PL+").splitAsStream(contents);
57
          show("wordsAnotherWay", wordsAnotherWay);
58
50
          try (Stream<String> lines = Files.lines(path))
68
61
          {
             show("lines", lines);
52
63
64
          Iterable<Path> iterable = FileSystems.getDefault().getRootDirectories();
65
```

```
Stream<Path> rootDirectories = StreamSupport.stream(iterable.spliterator(), false);
show("rootDirectories", rootDirectories);

Iterator<Path> iterator = Path.of("/usr/share/dict/words").iterator();
Stream<Path> pathComponents = StreamSupport.stream(Spliterators.spliteratorUnknownSize(
    iterator, Spliterator.ORDERED), false);
show("pathComponents", pathComponents);
}
```

#### API java.util.stream.Stream

- static <T> Stream<T> of(T... values)
   产生一个元素为给定值的流。
- static <T> Stream<T> empty()产生一个不包含任何元素的流。
- static <T> Stream<T> generate(Supplier<T> s)
   产生一个无限流,它的值是通过反复调用函数 s 而构建的。
- static <T> Stream<T> iterate(T seed, UnaryOperator<T> f)
- static <T> Stream<T> iterate(T seed, Predicate<? super T> hasNext, UnaryOperator<T> f)
   产生一个无限流,它的元素包含 seed、在 seed 上调用 f 产生的值、在前一个元素上调用 f 产生的值,等等。第一个方法会产生一个无限流,而第二个方法的流会在碰到第一个不满足 hasNext 谓词的元素时终止。
- static <T> Stream<T> ofNullable(T t)
   如果 t 为 null,返回一个空流,否则返回包含 t 的流。

# API java.util.Spliterators

static <T> Spliterator<T> spliteratorUnknownSize(Iterator<? extends T> iterator, int characteristics)

用给定的特性(一种包含诸如 Spliterator. ORDERED 之类的常量的位模式)将一个迭代器转换为一个具有未知尺寸的可分割的迭代器。

# API java.util.Arrays 12

• static <T> Stream<T> stream(T[] array, int startInclusive, int endExclusive) 8 产生一个流,它的元素是由数组中指定范围内的元素构成的。

# API java.lang.String

static Stream<String> lines() 11
 产生一个流,它的元素是由该字符串中的所有行构成的。

# API java.util.regex.Pattern

• Stream<String> splitAsStream(CharSequence input) 8 产生一个流,它的元素是输入中由该模式界定的部分。

#### API java.nio.file.Files

- static Stream<String> lines(Path path) 8
- static Stream<String> lines(Path path, Charset cs) 8
   产生一个流,它的元素是指定文件中的行,该文件的字符集为UTF-8,或者为指定的字符集。

#### API java.util.stream.StreamSupport

• static <T> Stream<T> stream(Spliterator<T> spliterator, boolean parallel) 产生一个流,它包含了由给定的可分割迭代器产生的值。

#### API java.Lang.Iterable

• Spliterator<T> spliterator() 8 为这个 Iterable 产生一个可分割的迭代器。默认实现不分割也不报告尺寸。

#### API java.util.Scanner

public Stream<String> tokens()
 产生一个字符串流,该字符串是调用这个扫描器的 next 方法时返回的。

## API java.util.function.Supplier<T> B

T get()提供一个值。

# 1.3 filter、map 和 flatMap 方法

流的转换会产生一个新的流,它的元素派生自另一个流中的元素。我们已经看到了filter转换会产生一个新流,它的元素与某种条件相匹配。下面,我们将一个字符串流转换为只包含长单词的另一个流:

List<String> words = . . .;
Stream<String> longWords = words.stream().filter(w -> w.length() > 12);

filter的引元是一个 Predicate<T> 类型的对象,即一个从 T 映射到 boolean 值的函数。

通常,我们想要按照某种方式来转换流中的值,此时,可以使用 map 方法并传递执行该转换的函数。例如,我们可以像下面这样将所有单词都转换为小写:

Stream<String> lowercaseWords = words.stream().map(String::toLowerCase);

这里,我们使用的是带有方法引用的 map,但是,通常我们可以使用 lambda 表达式来代替: Stream<String> firstLetters = words.stream().map(s -> s.substring(θ, 1));

上面的语句所产生的流中包含了所有单词的首字母。

在使用 map 时,会有一个函数应用到每个元素上,并且其结果是包含了应用该函数后所产生的所有结果的流。现在,假设我们有这样一个映射函数,它返回的是一个任意的结果或者多个结果。考虑下面这个示例,codePoints 方法会产生一个字符串中所有的编码点。例如,

codePoints("Hello \*\*)返回的流由 "H" "e" "l" "o" """ \*\* "构成。注意,地球符号(U+1F310)包含两个 char 值,所以 codePoints 方法必须费点事才能处理好它。我们马上就会看到几种具体实现方式。

codePoints 应该如何收集多个结果呢?对于流 API,最自然的方式是让方法返回一个Stream<String>对象。

假设我们将 codePoints 方法映射到一个字符串流上:

Stream<Stream<String>> result = words.stream().map(w -> codePoints(w));

那么会得到一个包含流的流,就像 [...["y","o","u","r"],["b","o","a","t"],...]。为了将其摊平为单个流 [..."y","o","u","r","b","o","a","t",...],可以使用 flatMap 方法而不是 map 方法:

```
Stream<String> flatResult = words.stream().flatMap(w -> codePoints(w));
// Calls codePoints on each word and flattens the results
```

既然我们已经了解了如何使用 codePoints 方法,那么应该如何编写它呢? String 类有一个 codePoints 方法,它会产生一个由整数编码点构成的流:

"Hello @".codePoints() // A stream of integers 72, 101, 108, 108, 111, 32, 127760

接下来,我们需要将每个整数都转换成一个字符串,其中包含了由给定的编码点构成的 Unicode 字符。遗憾的是,其技术实现是个难题。codePoints 方法产生了一个 IntStream,它与 Stream<Integer> 略有不同,正如你将在 1.13 节中所看到的。我们可以不使用 map, 而使用 mapToObj 方法来转换这些元素。也许你会觉得惊讶,就没有便捷的方法可以将一个整数编码点转换成一个字符串吗?下面是我能想到的最好的办法了:

```
public static Stream<String> codePoints(String s)
{
   return s.codePoints().mapToObj(cp -> new String(new int [] { cp }, θ, 1));
}
```

当使用 flatMap 时,你需要提供一个方法,它会为每一个流元素产生一个新的流。正如你所见,这会显得很冗长,而且效率也略显低下。mapMulti 方法提供了另一种选择。与产生由结果构成的流不同,我们生成结果后将它们传递给一个收集器,即一个实现了 Consumer 函数式接口的类的对象。每一个结果都会调用该收集器上的 accept 方法。

让我们来实践一下,下面的循环会产生字符串 s 的编码点:

```
int i = 0;
while (i < s.length())
{
   int cp = sentence.codePointAt(i);
   // Do something with cp
   if (Character.isSupplementaryCodePoint(cp)) i += 2;
   else i++;
}</pre>
```

当调用 mapMulti 时,你需要提供一个用流元素和收集器调用的函数。该函数会将结果传递给收集器。

```
Stream<String> result = words.stream().mapMulti((s, collector) ->
{
    int i = 0;
    while (i < s.length())
    {
        int cp = sentence.codePointAt(i);
        collector.accept(cp);
        if (Character.isSupplementaryCodePoint(cp)) i += 2;
        else i++;
    }
});</pre>
```

#### API java.util.stream.Stream

- Stream<T> filter(Predicate<? super T> predicate)
   产生一个流,它包含当前流中所有满足谓词条件的元素。
- <R> Stream<R> map(Function<? super T,? extends R> mapper)
  产生一个流,它包含将 mapper 应用于当前流中所有元素所产生的结果。
- <R> Stream<R> flatMap(Function<? super T,? extends Stream<? extends R>> mapper) 产生一个流,它是通过将 mapper 应用于当前流中所有元素所产生的结果连接到一起而 获得的。(注意,这里的每个结果都是一个流。)
- <R> Stream
   mapMulti(BiConsumer<? super T,? super Consumer<R>> mapper) 16
   每一个流元素都会调用 mapper, 并且所有在调用期间传递给 Consumer 的元素都会被添加到结果流中。

# 1.4 抽取子流和组合流

调用 stream.limit(n) 会返回一个新的流,它在 n 个元素之后结束(如果原来的流比 n 短,那么就会在该流结束时结束)。这个方法对于裁剪无限流的尺寸特别有用。例如,

Stream<Double> randoms = Stream.generate(Math::random).limit(100);

会产生一个包含 100 个随机数的流。

调用 stream. skip(n) 正好相反:它会丢弃前 n 个元素。这个方法对于本书的读操作示例很方便,因为按照 split 方法的工作方式,第一个元素是没什么用的空字符串。我们可以通过调用 skip 来跳过它:

Stream<String> words = Stream.of(contents.split("\\PL+")).skip(1);

stream.takeWhile(predicate)调用会在谓词为真时获取流中的所有元素,然后停止。例如,假设我们使用上一节的 codePoints 方法将字符串分割为字符,然后想要收集所有的数字元素,那么 takeWhile 方法可以实现此目标:

```
Stream<String> initialDigits = codePoints(str).takeWhile(
    s -> "0123456789".contains(s));
```

dropWhile 方法的做法正好相反,它会在条件为真时丢弃元素,并产生一个由第一个使该条件为假的字符开始的所有元素构成的流:

Stream<String> withoutInitialWhiteSpace = codePoints(str).dropWhile(
 s -> s.trim().length() == 0);

我们可以用 Stream 类的静态 concat 方法将两个流连接起来:

Stream<String> combined = Stream.concat(
 codePoints("Hello"), codePoints("World"));
 // Yields the stream ["H", "e", "l", "l", "o", "W", "o", "r", "l", "d"]

当然,第一个流不应该是无限的,否则第二个流永远都不会有机会得到处理。

#### API java.util.stream.Stream

- Stream<T> limit(long maxSize)
   产生一个流,其中包含当前流中最初的 maxSize 个元素。
- Stream<T> skip(long n)
   产生一个流,它的元素是当前流中除了前 n 个元素之外的所有元素。
- Stream<T> takeWhile(Predicate<? super T> predicate) 9 产生一个流,它的元素是当前流中所有满足谓词条件的元素。
- Stream<T> dropWhile(Predicate<? super T> predicate) 9 产生一个流,它的元素是当前流中排除不满足谓词条件的元素之外的所有元素。
- static <T> Stream<T> concat(Stream<? extends T> a, Stream<? extends T> b) 产生一个流,它的元素是 a 的元素后面跟着 b 的元素。

# 1.5 其他的流转换

distinct 方法会返回一个流,它的元素是从原有流中产生的,即原来的元素按照同样的顺序剔除重复元素后产生的。这些重复元素并不一定是毗邻的。

```
Stream<String> uniqueWords
```

对于流的排序,有多种 sorted 方法的变体可用。其中一种用于操作 Comparable 元素的流,而另一种可以接受一个 Comparator。下面,我们对字符串排序,使得最长的字符串排在最前面:

```
Stream<String> longestFirst
```

与所有的流转换一样,sorted 方法会产生一个新的流,它的元素是原有流中按照顺序排列的元素。

当然,我们在对集合排序时可以不使用流。但是,当排序处理是流管道的一部分时, sorted 方法就会显得很有用。

最后, peek 方法会产生另一个流, 它的元素与原来流中的元素相同, 但是在每次获取一个元素时, 都会调用一个函数。这对于调试来说很方便:

```
Object[] powers = Stream.iterate(1.0, p -> p * 2)
   .peek(e -> System.out.println("Fetching " + e))
   .limit(20).toArray();
```

*当实际访问一个元 时 就会打印出来一条消息。 方式 你可以验证iterate 回 无 流是 惰性处 。*

 *提 当我们使 器来 流 序时 可以 对各个流 换操作中 某一 个 在它所 方法中 断点。对于大多数IDE,我们 可以在lambda 式中 断点。如果只想了 在流 某个 定点上会发 什么 么可以添加下 代 并在 二 上设置断点*

```
.peek(x •>
   {
       return;
   })
```

# *ah<sup>|</sup> java.util.stream.St ream*

- *• Stream<T> distinct!) 产 一个流 包含当前流中所有不同 元 。*
- *<sup>參</sup> Stream<T> sorted()*
- *• Stream<T> sorted (Comparator? super T> comparator) 产 一个流 它 元 是当前流中 所有元 按照 序排列 。 一个方法 求元 是实 了 Comparable的类的实例。*
- *• Stream<T> peek(Consumer<? super T> action) 产 一个流 它与当前流中 元 同 在 取其中每个元 时 会将其传 action。*

# *1.6 <sup>单</sup>*

*在你已 到了如何创建和 换流 我们 于可以 最 内容了 即从流数 据中 得 案。我们在本 所 方法 为 (reduction) 是一 操作 (terminal operation),它们会将流 为可以在 序中使 流值。*

*你已 到 一 单 count方法会 回流中元 数ft。*

*其他 单 有max和min,它们分別 回最大值和最小值。 作 些 方法 冋 是一个 型为Optional<T> 值 它 么在其中包 了 案 么 没有任何值 (因为流 巧为 )。在 去 到 情况 回null是很常见的 但是 样做会导 在未做 完备测 序中产 指 异常。Optional 型是一 来 少 回值 更好方式。 我们将在下一 中 Optional 型。下 展 了如何 得流中 最大值*

```
Optional<String> largest = words.max(String::compareToIgnoreCase):
System.out.printin("largest: + largest.orElseC*"));
```

*findFirst <sup>回</sup> <sup>是</sup> 合中 一个值 <sup>它</sup> 常在与filter 合使 时很有 。<sup>例</sup> 如 下 展 了如何找到 一个以字母Q开头 单 前提是存在 样 单*

```
Optional<String> startsWithQ
   :words.filter(s -> s.startsWith("Q")).findFirst();
```

*如果不强 使 一个匹 是使 任意 匹 可以 么就可以使 findAny方 法。 个方法在并 处 流时很冇效 因为流可以报告任何它找到 匹 不是 制为必 报告 一个匹 。*

*OptionaUString startsWithQ*

*=words.parallel().fliter(<sup>s</sup> -> s.startsWith("Q")).findAny();*

*如果只想 是否存在匹 么可以使 anyMatcho 个方法会接受一个 引元, 因此不需要使 filter。*

*boolean aWordStartsWithQ*

*=words.paraUel().anyMatch(s ■> s.startsWith("QB));*

*有aUMatch和noneMatch方法 它们分别在所有元 和没有任何元 匹 情况 下 回true 些方法也可以 并 。*

# *java.util.stream.Stream*

- *• Optional<T> max (Comparator? super T> comparator)*
- *• Optional<T> min(Compa ator<? super T> comparator) 分别产 个流 最大元 和最小元 使 定比 器定义 排序 则 如果 个流为 会产 一个 Optional对 。 些操作 是 操作。*
- *• Optional<T> findFirstO*
- *• Optional<T> findAny() 分别产 个流 一个和任意一个元 如果 个流为 会产 一个 Optional 对 。 些操作 是终结操作。*
- *• boolean anyMatch(Predicated super T> predicate)*
- *• boolean allMatch(Predicate<? super T> predicate)*
- *• boolean noneMatch(Predicate<? super T> predicate) 分别在 个流中任意元 、所有元 和没有任何元 匹 定 时 回true。这些 操作 是 操作。*

# *1.7 Optional 型*

*Optional<T>对 是一 包 器对 么包 了 型T 对 么没有包 任何对 。对于 一 情况 我们称这种值是存在 。Optional<T> 型 当作一 更安全 方式, 来替代 型T 引 引 么引 某个对 么为null 但是 它只有在正 使 用的情况下才会更安全 接下来 三个小 我们将 如何正 使 。*

# *1.7.1 <sup>取</sup> 0ptional <sup>值</sup>*

*有效地使 Optional 关 是 使 样 方法 它在值不存在 情况下会产 一个可 替代 只有在值存在 情况下才会使用这个值。*

*本小 我们先来 一条 。 常 在没有任何匹 时 我们会希望使 某 值 可 是 字 串*

```
String result » optionalString.orElse(^);
  // The wrapped string, or if none
```

*你 可以 代 来 值*

*String result <sup>=</sup> optionalString.orElseGet(() -> System.getProperty("myapp.default")): // The function is only called when needed*

#### *或 可以在没有任何值时抛出异常*

```
String result =叩tionalString.orElseThrow(IllegalStateException::new);
  // Supply a aethod that yields an exception object
```

## *<sup>a</sup>«] java.util.Optional*

- *• <sup>T</sup> orElse(T other) 产 个Optional 值 或 在 Optional为 时 产 other*
- *• <sup>T</sup> orElseGet(Supplier<? extends T> other) 产生这个Optional 值 或 在 Optional为 时 产 othe「的结果。*
- *• <X extends Throwable> <sup>T</sup> orElseThrow(Supplier<? extends X> exceptionSuppUer) 产 个Optional 值 或 在 Optional为 时 抛出 exceptionsupplier 果。*

# *1.7.2 消 Optional 值*

*在上一小 我们 到了如何在不存在任何值 情况下产 应 替代 。另一条使 可 值 是只有在其存在 情况下才消 值。*

*ifPresent方法会接受一个函数。如果可 值存在 么它会 传 函数。否则 不 会发 任何事情。*

```
叩tionalValue. ifPresent (v •> Process v);
```

*例如 如果在 值存在 情况下想 将其添加到某个 中 么就可以 optionalValue.ifPresent(v -> results.add(v));*

# *或 接*

```
optionalValue•ifPresent(results :add);
```

*如果想 在可 值存在时执 一 动作 在可 值不存在时执 另一 动作 可以使 ifPresentOrElse*

```
optionalValue.ifPresentOrElse(
  v -> System.out.printin(■Found + v),
   ()-> logger.warningC'No match-));
```

# *gjava.util.Optional*

- *• void ifPresent(Consumer<? super T> action) 如果 Optional不为 就将它 值传 action。*
- *• void ifPresentOrElse(Consumer<? super T> action, Runnable emptyAction)*

*如果 Optional不为 就将它 值传 action,否则 emptyAction*

# *1.7.3 化 Optional 值*

*在上一 中 你 到了如何从Optional对 中 取值。另一 有 是保持 Optional完整 使 map方法来 换Optional内 值*

*Optional<String> transformed = optionalString.map(String::toUpperCase);*

*如果optionalString为 么transformed也为 。*

*下 是另一个例子 我们将一个 果添加到列 中 如果它存在*

*optionalValue.map(results::add);*

*如果叩tionalValue为 则什么也不会发 <sup>o</sup>*

*0 <sup>注</sup> <sup>个</sup>map方法与1.3 中描述的Stream接口 map方法 <sup>似</sup>。你可以 接将可 值想 成尺寸为0或1 流。 果 尺寸也是0或<sup>1</sup> 并且在后一 情况中 函数 会应 于其上。*

*似地 可以使 filter方法来只处 些在 换它之前或之后满 <sup>某</sup> 定属性 Optional值。如果不满 属性 么 会产 果*

*Optional<String transformed = optionalString .filter(s •> s.length() >= 8) •map(String::toUpperCase);*

*你也可以 or方法将 Optional替换为一个可替代 Optional。 个可替代值将以惰性 方式 。*

*Optional<String> result <sup>=</sup> optionalString.or(() •> // Supply an Optional alternatives.stream() findFirst());*

*如M optionalString 值存在 么result为optionalString。如果值不存在 么就会 计算lambda 式 并使 出来 果。*

# *ah] java.util.Optional*

- *• <U> Optional<U> map(Function<? super T,? extends U> mapper) 产 一个Optional,如果当前 Optional 值存在 么所产 Optional 值是 将 定 函数应 于当前 Optional 值 得到 否则 产 一个 Optional*
- *• Optional<T> filter!Predicate<? super T> predicate) 产 一个Optional,如果当前 Optional 值满 定 条件 么所产 Optional 值就是当前Optional 值 否则 产 一个 Optional。*
- *• Optional<T> or(Supplier<? extends Optional? extends T» supplier) 如果当前Optional不为 则产 当前 Optional 否则 s叩plie「产 一个Optional*

# *1.7.4不 合使 Optional<sup>值</sup> 方式*

*如果没有正 地使 Optional<sup>值</sup> <sup>么</sup> 比以往得到"<sup>某</sup> <sup>或</sup>null" 方式 你并没有*

### *得到任何好处。*

*get方法会在Optional值存在 情况下 得其中包 元 或 在不存在 情况下抛 出一个NoSuchElementException 异常。因此*

*Optional<T> optionalValue =...; optionalValue.get().someMethod()*

### *并不比下 方式更安全*

*<sup>丁</sup> value =.. value. someMethodO;*

*isPresent方法和isEmpty方法会报告某个Optional<T>对 是否具有值。但是*

*if (叩tionalValue. isPresent())叩tionalValue. get0. sorneHethod();*

#### *并不比下 方式更容易处*

*if (value != null) value.someMethodU;*

*KI<sup>注</sup> Java <sup>10</sup>为get方法引入了一个 人听 同义 --- orElseThrow 当调用optionalValue.orElseThrowO.someMethod()<sup>时</sup> 如果optionalValue <sup>为</sup> <sup>么</sup> <sup>个</sup> 就会产 一个异常。 样命名是希望 序员只有在明 地 情况不会发 时 才去使 orElseThrow。*

*下 是一些有关Optional 型正 法 提*

- *• Optional 型 变 永 不应 为null*
- *不 使 Optional 型 域。因为其代价是 外多出来一个对 。在类的内 应 使 nuU表示缺失 域更易于操作。如果不希望使 Optional 型 域 么就 是不可序列化 。*
- *型为Optional 方法参数是有 。在很多常 求值必 存在 情况下 对 它们的调用会令人不快。应 写 方法 两个 本 分别是包含和不包含 参数 本。(另外 回Optional对 是没 因为它是一 函数可 没有 果 恰当方式。)*
- *不 在 合中放 Optional对 并且不 将它们 作map的键。应 接收 其中 值。*

# *mj] java. util.Optional*

- *• <sup>T</sup> get()*
- *• <sup>T</sup> orElseThrow() 1O 产 个Optional 值 或 在 Optional为 时 抛出一个NoSuchElementException 异常。*
- *<sup>參</sup> boolean isEmpty()*
- *• boolean isPresent()*

*分别对应 Optional为 和不为 时 回true*

#### 1.7.5 创建 Optional 值

到目前为止,我们已经讨论了如何使用其他人创建的 Optional 对象。如果想要编写方法来创建 Optional 对象,那么有多个方法可以用于此目的,包括 Optional.of(result)和 Optional.empty()。例如,

```
public static Optional<Double> inverse(Double x)
{
   return x == 0 ? Optional.empty() : Optional.of(1 / x);
}
```

ofNullable 方法被用来作为可能出现的 null 值和可选值之间的桥梁。Optional.ofNullable(obj) 会在 obj 不为 null 的情况下返回 Optional.of(obj), 否则会返回 Optional.empty()。

#### API java.util.Optional

- static <T> Optional<T> of(T value)
- static <T> Optional<T> ofNullable(T value)
   用给定值产生一个 Optional。如果 value 为 null,那么第一个方法会抛出一个 NullPointerException 异常,而第二个方法会产生一个空 Optional。
- static <T> Optional<T> empty()
   产生一个空 Optional。

## 1.7.6 用 flatMap 构建 Optional 值的函数

假设你有一个可以产生 Optional<T> 对象的方法 f, 并且目标类型 T 具有一个可以产生 Optional <D> 对象的方法 g。如果它们都是普通的方法,那么你可以通过调用 s.f().g()来将它们组合起来。但是这种组合无法工作,因为 s.f()的类型为 Optional<T>,而不是 T。因此,需要调用

Optional<U> result = s.f().flatMap(T::g);

如果 s.f()的值存在,那么 g 就可以应用到它上面。否则,就会返回一个空 Optional <U>。 很明显,如果有更多可以产生 Optional 值的方法或 lambda 表达式,那么就可以重复此过程。你可以直接将对 flatMap 的调用链接起来,从而构建由这些步骤构成的管道,只有所有步骤都成功,该管道才会成功。

例如,考虑前一节中安全的 inverse 方法。假设我们还有一个安全的平方根:

```
public static Optional<Double> squareRoot(Double x)
{
   return x < 0 ? Optional.empty() : Optional.of(Math.sqrt(x));
}</pre>
```

那么你可以像下面这样计算倒数的平方根:

Optional<Double> result = inverse(x).flatMap(MyMath::squareRoot);

或者, 你可以选择下面的方式:

```
Optional<Double> result = Optional.of(-4.0).flatMap(Demo::inverse).flatMap(Demo::squareRoot);
```

18

无论是 inverse 方法还是 squareRoot 方法返回 Optional.empty(),整个结果都会为空。

注释: 你已经在 Stream 接口中看到过 flatMap 方法 (参见 1.3 节), 当时,这个方法将一个产生流的方法映射到了流的所有元素上,然后将所产生的由流构成的流摊平。 Optional.flatMap 方法与其操作方式一样,通过将产生 Optional 的方法映射到 Optional 上,就会得到由 Optional 构成的 Optional,然后将其摊平。

#### API java.util.Optional 8

• <U> Optional<U> flatMap(Function<? super T,? extends Optional<? extends U>> mapper) 如果 Optional 存在,产生将 mapper 应用于当前 Optional 值所产生的结果,或者在当前 Optional 为空时,返回一个空 Optional。

## 1.7.7 将 Optional 转换为流

stream 方法会将一个 Optional<T> 对象转换为一个具有 0 个或 1 个元素的 Stream<T> 对象。这种做法看起来很自然,但是我们为什么希望这么做呢?

这会使返回 Optional 结果的方法变得很有用。假设我们有一个用户 ID 流和下面的方法: Optional <user> lookup(String id)

怎样才能在获取用户流时, 跳过那些无效的 ID 呢?

当然, 我们可以过滤掉无效 ID, 然后将 get 方法应用于剩余的 ID:

Stream<String> ids = . . .;

Stream<User> users = ids.map(Users::lookup)

- .filter(Optional::isPresent)
- .map(Optional::get);

但是这样就需要使用我们之前警告过要慎用的 isPresent 和 get 方法。下面的调用显得更优雅:

Stream<User> users = ids.map(Users::lookup)
 .flatMap(Optional::stream);

每一个对 stream 的调用都会返回一个具有 0 个或 1 个元素的流。flagMap 方法将这些流组合在一起,这意味着不存在的用户会直接被丢弃。

註釋:本节我们研究了一些令人愉快的场景,在其中我们拥有可以返回 Optional 值的方法。当前,许多方法都会在没有任何有效结果的情况下返回 null。假设 Users.classicLookup(id)会返回一个 User 对象或者 null,而不是 Optional <User>,我们当然可以过滤掉 null 值:

Stream<User> users = ids.map(Users::classicLookup)
 .filter(Objects::nonNull);

但是如果更喜欢 flatMap 的方式,那么我们可以使用下面的代码:

Stream<User> users = ids.flatMap(
 id -> Stream.ofNullable(Users.classicLookup(id)));

#### 或者是下面的代码:

```
Stream<User> users = ids.map(Users::classicLookup)
   .flatMap(Stream::ofNullable);
```

Stream.ofNullable(obj) 这个调用在 obj 为 null 时,会产生一个空的流,否则会产生一个只包含 obj 的流。

程序清单 1-3 中的示例程序演示了 Optional API 的使用方式。

#### 程序清单 1-3 optional/OptionalTest.java

```
1 package optional;
2
3 import java.io.*;
4 import java.nio.file.*;
5 import java.util.*;
7
    * @version 1.02 2019-08-28
    * @author Cay Horstmann
18
   public class OptionalTest
11
12
      public static void main(String[] args) throws IOException
13
14
         var contents = Files.readString(
15
            Path.of("../gutenberg/alice30.txt"));
16
         List<String> wordList = List.of(contents.split("\\PL+"));
17
18
         Optional<String> optionalValue = wordList.stream()
19
            .filter(s -> s.contains("fred"))
20
            .findFirst();
21
         System.out.println(optionalValue.orElse("No word") + " contains fred");
22
23
         Optional<String> optionalString = Optional.empty();
24
         String result = optionalString.orElse("N/A");
25
         System.out.println("result: " + result);
26
         result = optionalString.orElseGet(() -> Locale.getDefault().getDisplayName());
27
         System.out.println("result: " + result);
28
         try
29
38
            result = optionalString.orElseThrow(IllegalStateException::new);
31
            System.out.println("result: " + result);
32
33
         catch (Throwable t)
         {
35
36
            t.printStackTrace();
37
38
         optionalValue = wordList.stream()
39
             .filter(s -> s.contains("red"))
48
             .findFirst();
41
         optionalValue.ifPresent(s -> System.out.println(s + " contains red"));
42
43
```

```
var results = new HashSet<String>();
44
         optionalValue.ifPresent(results::add);
45
         Optional < Boolean > added = optional Value.map(results::add);
46
         System.out.println(added);
47
48
         System.out.println(inverse(4.0).flatMap(OptionalTest::squareRoot));
49
         System.out.println(inverse(-1.0).flatMap(OptionalTest::squareRoot));
58
         System.out.println(inverse(0.0).flatMap(OptionalTest::squareRoot));
51
         Optional<Double> result2 = Optional.of(-4.0)
52
             .flatMap(OptionalTest::inverse).flatMap(OptionalTest::squareRoot);
53
         System.out.println(result2);
54
      }
55
56
      public static Optional<Double> inverse(Double x)
57
58
         return x == 0 ? Optional.empty() : Optional.of(1 / x);
59
68
61
      public static Optional<Double> squareRoot(Double x)
62
63
         return x < 0 ? Optional.empty() : Optional.of(Math.sqrt(x));
64
65
66 }
```

#### API java.util.Optional

<u> Optional<u> flatMap(Function<? super T,Optional<u>> mapper)
 产生将 mapper 应用于当前 Optional 值的结果,或者在当前 Optional 为空时,返回一个空 Optional。

# 1.8 收集结果

当处理完流之后,通常会想要查看其结果。此时可以调用 iterator 方法,它会产生用来访问元素的旧式风格的迭代器。

或者,可以调用 forEach 方法,将某个函数应用于每个元素:

stream.forEach(System.out::println);

在并行流上,forEach 方法会以任意顺序遍历各个元素。如果想要按照流中的顺序来处理它们,可以调用 forEachOrdered 方法。当然,这个方法会丧失并行处理的部分甚至全部优势。

但是,更常见的情况是,我们想要将结果收集到数据结构中。此时,可以调用 toList,获得由流的元素构成的列表。

调用 toArray 可以获得由流的元素构成的数组。

因为无法在运行时创建泛型数组,所以表达式 stream.toArray()会返回一个 Object[]数组。如果想要让数组具有正确的类型,可以向其传递数组构造器:

```
String[] result = stream.toArray(String[]::new);
// stream.toArray() has type Object[]
```

针对将流中的元素收集到另一个目标中的需求,有一个便捷方法 collect 可用,它会接受

一个 Collector 接口的实例。收集器是一种收集众多元素并产生单一结果的对象, Collectors 类提供了大量用于生成常见收集器的工厂方法。在 toList 方法被添加到 Java 16 之前, 我们必须使用 Collectors.toList() 生成的收集器:

List<String> result = stream.collect(Collectors.toList());

类似地,下面的代码展示了如何将流的元素收集到一个集中:

Set<String> result = stream.collect(Collectors.toSet());

这些调用会返回一个列表或集,但是也就仅此而已。集合有可能并非可变的、可序列化的或线程安全的。如果想要控制获得的集的种类,那么可以使用下面的调用:

TreeSet<String> result = stream.collect(Collectors.toCollection(TreeSet::new));

假设想要通过连接操作来收集流中的所有字符串。我们可以调用

String result = stream.collect(Collectors.joining());

如果想要在元素之间增加分隔符,可以将分隔符传递给 joining 方法:

String result = stream.collect(Collectors.joining(", "));

如果流中包含除字符串以外的其他对象,那么我们需要先将其转换为字符串,就像下面这样:
String result = stream.map(Object::toString).collect(Collectors.joining(", "));

如果想要将流的结果约简为总和、数量、平均值、最大值或最小值,可以使用 summarizing (Int|Long|Double) 方法中的某一个。这些方法会接受一个将流对象映射为数值的函数,产生类型为 (Int|Long|Double) Summary Statistics 的结果,同时计算总和、数量、平均值、最大值和最小值。

```
IntSummaryStatistics summary = stream.collect(
   Collectors.summarizingInt(String::length));
double averageWordLength = summary.getAverage();
double maxWordLength = summary.getMax();
```

程序清单 1-4 中的示例程序展示了如何从流中收集元素。

#### 程序清单 1-4 collecting/CollectingResults.java

```
package collecting;
2
3 import java.io.*;
4 import java.nio.file.*;
5 import java.util.*;
6 import java.util.stream.*:
7
8 /**
   * @version 1.02 2019-08-28
9
10 * @author Cay Horstmann
11 */
12 public class CollectingResults
13 {
      public static Stream<String> noVowels() throws IOException
14
15
         var contents = Files.readString(
16
```

```
Path.of("../gutenberg/alice30.txt"));
17
18
         List<String> wordList = List.of(contents.split("\\PL+"));
19
         Stream<String> words = wordList.stream();
20
         return words.map(s -> s.replaceAll("[aeiouAEIOU]", ""));
21
22
23
      public static <T> void show(String label, Set<T> set)
24
25
         System.out.print(label + ": " + set.getClass().getName());
26
         System.out.println("["
27
            + set.stream().limit(10).map(Object::toString).collect(Collectors.joining(", "))
28
29
            + "]");
      }
30
31
      public static void main(String[] args) throws IOException
32
33
         Iterator<Integer> iter = Stream.iterate(0, n -> n + 1).limit(10).iterator();
34
         while (iter.hasNext())
35
             System.out.println(iter.next());
36
37
          Object[] numbers = Stream.iterate(0, n -> n + 1).limit(10).toArray();
38
          System.out.println("Object array:" + numbers);
30
             // Note it's an Object[] array
48
41
42
         try
43
             var number = (Integer) numbers[θ]; // OK
44
             System.out.println("number: " + number);
45
             System.out.println("The following statement throws an exception:");
             var numbers2 = (Integer[]) numbers; // Throws exception
47
48
          }
          catch (ClassCastException e)
49
SA
             System.out.println(e);
51
52
53
          Integer[] numbers3 = Stream.iterate(0, n -> n + 1)
54
             .limit(10)
55
             .toArray(Integer[]::new);
56
57
          System.out.println("Integer array: " + numbers3);
             // Note it's an Integer[] array
58
59
          Set<String> noVowelSet = noVowels().collect(Collectors.toSet());
68
          show("noVowelSet", noVowelSet);
61
62
          TreeSet<String> noVowelTreeSet = noVowels().collect(
63
             Collectors.toCollection(TreeSet::new));
64
          show("noVowelTreeSet", noVowelTreeSet);
65
56
          String result = noVowels().limit(10).collect(Collectors.joining());
67
          System.out.println("Joining: " + result);
68
          result = noVowels().limit(10)
69
              .collect(Collectors.joining(", "));
78
          System.out.println("Joining with commas: " + result);
71
```

```
72
         IntSummaryStatistics summary = noVowels().collect(
73
            Collectors.summarizingInt(String::length));
74
         double averageWordLength = summary.getAverage();
75
         double maxWordLength = summary.getMax();
76
         System.out.println("Average word length: " + averageWordLength);
77
         System.out.println("Max word length: " + maxWordLength);
78
         System.out.println("forEach:");
79
         noVowels().limit(10).forEach(System.out::println);
      }
81
82 }
```

#### API java.util.stream.BaseStream

• Iterator<T> iterator() 产生一个用于获取当前流中各个元素的迭代器。这是一种终结操作。

#### API java.util.stream.Stream

- List<T> toList() 16 产生一个由这个流中所有元素构成的列表。
- void forEach(Consumer<? super T> action)
   在流的每个元素上调用 action。
- Object[] toArray()
- <A> A[] toArray(IntFunction<A[]> generator)
   产生一个对象数组,或者在传递了构造器引用 A[]::new 时,返回一个 A 类型的数组。
   这些操作都是终结操作。
- <R,A> R collect(Collector<? super T,A,R> collector)
   使用给定的收集器来收集当前流中的元素。Collectors 类有用于多种收集器的工厂方法。

# API java.util.stream.Collectors

- static <T> Collector<T,?,List<T>> toList()
- static <T> Collector<T,?,List<T>> toUnmodifiableList() 10
- static <T> Collector<T,?,Set<T>> toSet()
- static <T> Collector<T,?,Set<T>> toUnmodifiableSet() 10 产生一个将元素收集到列表或集合中的收集器。
- static <T,C extends Collection<T>> Collector<T,?,C> toCollection(Supplier<C> collectionFactory) 产生一个将元素收集到任意集合中的收集器。可以传递一个诸如 TreeSet::new 的构造器引用。
- static Collector<CharSequence,?,String> joining()
- static Collector<CharSequence,?,String> joining(CharSequence delimiter)
- static Collector<CharSequence,?,String> joining(CharSequence delimiter, CharSequence prefix, CharSequence suffix)

产生一个连接字符串的收集器。分隔符 (delimiter) 会置于字符串之间, 而第一个字

*串之前可以有前 (prefix),最后一个字 串之后可以有后 (suffix)。如果没有指 定 么它们 为 。*

- *• static <T> Collectors,?,IntSummaryStatistics> summarizinglnt(ToIntFunction<? super T> mapper)*
- *• static <T> CoUector<T,?,LongSummaryStatistics> summarizingLong(ToLongFunction<? super T> mapper)*
- *• static <T> CoUector<T,?,Doubles naryStatistics> su arizingDouble(ToDoubleFunction<? super T> mapper)*

*产 够 成(Int|Long|Double)SunmaryStatistics对 收 器 它们可以 得将 mapper应 于每个元 后所产 果 数 、总和、平均值、最大值和最小值。*

# *<sup>j</sup> IntSummaryStatistics LongSumaryStatistics Doubles umry Statistics*

- *• long getCountO 产 汇总后 元 个数。*
- *• (intI long|double) getSum()*
- *• double getAveragef) 产 汇总后 元 总和或平均值 或 在没有任何元 时 回0<sup>o</sup>*
- *• (inti long <sup>I</sup> double) getMaxO*
- *• (intI long <sup>I</sup> double) getMin() 产 汇总后 元 最大值和最小值 或 在没有任何元 时 产 (Integer| Long| Double).(MAX|MIN)\_VALUE<sup>o</sup>*

# *1.9<sup>收</sup> 到映射 <sup>中</sup>*

*假 我们有一个StreanKPerson 并且想 将其元 收 到一个映射 中 样后 就 可以 它们 ID来査找人员了。Collectors.toMap方法有两个函数引元 它们 来产 映 射 和值。例如*

```
public record Person(int idt String name) {}
0 • •
Map<Integer, String> idToName = people.collect(
   Collectors.toMap(Person::id, Person::name));
```

*常情况下 值应 是实 元 因此 2个函数可以使 Function.identity()。*

```
Map<Integer, Person> idToPerson = people.collect(
   Collectors.toMap(Person::id, Function.identity()));
```

*如果有多个元 具有 同 就会存在冲 收 器将会抛出一个IllegalStateException异常。可以通过提供 3个函数引元来 为 函数会 对 定 已有 值和新值来 决冲 并 定 对应 值。 个函数应 回已有值、新值或它们 合。*

在下面的代码中,我们构建了一个映射表,存储了所有可用 locale 中的语言,其中每种语言在默认 locale 中的名字(例如"German")为键,而其本地化的名字(例如"Deutsch")为值:

```
Stream<Locale> locales = Stream.of(Locale.getAvailableLocales());
Map<String, String> languageNames = locales.collect(
   Collectors.toMap(
        Locale::getDisplayLanguage,
        loc -> loc.getDisplayLanguage(loc),
        (existingValue, newValue) -> existingValue));
```

我们不关心同一种语言是否可能会出现两次(例如,德国和瑞士都使用德语),因此我们只记录第一项。

直 注释:在本章中,我们使用 Locale 类作为感兴趣的数据集的数据源。请参阅第7章以了解有关 locale 的更多信息。

现在,假设我们想要了解给定国家的所有语言,这样我们就需要一个 Map<String, Set<String>>。例如,"Switzerland" 的值是集 [French, German, Italian]。首先,我们为每种语言都存储一个单例集。无论何时,只要找到了给定国家的新语言,我们就会对已有集和新集进行并操作。

```
Map<String, Set<String>> countryLanguageSets = locales.collect(
   Collectors.toMap(
        Locale::getDisplayCountry,
        l -> Collections.singleton(l.getDisplayLanguage()),
        (a, b) ->
        { // Union of a and b
            var union = new HashSet<String>(a);
            union.addAll(b);
            return union;
        }));
```

在下一节中, 你将会看到一种更简单的获取这种映射表的方式。

如果想要得到 TreeMap, 那么可以将构造器作为第 4 个引元来提供。你必须提供一种合并函数。下面是本节一开始所列举的示例之一,现在它会产生一个 TreeMap:

```
Map<Integer, Person> idToPerson = people.collect(
   Collectors.toMap(
        Person::id,
        Function.identity(),
        (existingValue, newValue) -> { throw new IllegalStateException(); },
        TreeMap::new));
```

i 注释:对于每一个 toMap 方法,都有一个等价的可以产生并发映射表的 toConcurrentMap 方法。单个并发映射表可以用于并行集合处理。当使用并行流时,共享的映射表比合并映射表更高效。注意,元素不再是按照流中的顺序收集的,但是通常这不会有什么问题。

程序清单 1-5 给出了将流的结果收集到映射表中的示例。

#### 程序清单 1-5 collecting/CollectingIntoMaps.java

```
package collecting;
2
3 import java.io.*;
4 import java.util.*;
5 import java.util.function.*;
   import java.util.stream.*;
8
   * @version 1.01 2021-09-06
9
   * @author Cay Horstmann
10
   public class CollectingIntoMaps
13
14
      public record Person(int id, String name) {}
15
16
      public static Stream<Person> people()
17
18
19
         return Stream.of(new Person(1001, "Peter"), new Person(1002, "Paul"),
            new Person(1003, "Mary"));
20
21
22
      public static void main(String[] args) throws IOException
23
24
         Map<Integer, String> idToName = people().collect(
25
            Collectors.toMap(Person::id, Person::name));
26
         System.out.println("idToName: " + idToName);
27
28
         Map<Integer, Person> idToPerson = people().collect(
29
            Collectors.toMap(Person::id, Function.identity()));
30
         System.out.println("idToPerson: " + idToPerson.getClass().getName()
31
            + idToPerson);
32
33
         idToPerson = people().collect(
34
            Collectors.toMap(Person::id, Function.identity(),
35
                (existingValue, newValue) -> { throw new IllegalStateException(); },
36
               TreeMap::new));
37
         System.out.println("idToPerson: " + idToPerson.getClass().getName()
38
            + idToPerson);
39
48
         Stream<Locale> locales = Stream.of(Locale.getAvailableLocales());
41
         Map<String, String> languageNames = locales.collect(
42
            Collectors.toMap(
43
               Locale::getDisplayLanguage,
44
               l -> l.getDisplayLanguage(l),
45
                (existingValue, newValue) -> existingValue));
46
         System.out.println("languageNames: " + languageNames);
47
48
         locales = Stream.of(Locale.getAvailableLocales());
49
          Map<String, Set<String>> countryLanguageSets = locales.collect(
58
51
             Collectors.toMap(
                Locale::getDisplayCountry,
52
                l -> Set.of(l.getDisplayLanguage()),
53
```

```
(a, b) ->
54
                   { // union of a and b
55
                      Set<String> union = new HashSet<>(a);
56
                      union.addAll(b);
57
                      return union;
58
59
         System.out.println("countryLanguageSets: " + countryLanguageSets);
68
      }
61
62 }
```

#### API java.util.stream.Collectors

- static <T,K,U> Collector<T,?,Map<K,U>> toMap(Function<? super T,? extends K> keyMapper, Function<? super T,? extends U> valueMapper)
- static <T,K,U> Collector<T,?,Map<K,U>> toMap(Function<? super T,? extends K> keyMapper, Function<? super T,? extends U> valueMapper, BinaryOperator<U> mergeFunction)
- static <T,K,U,M extends Map<K,U>> Collector<T,?,M> toMap(Function<? super T,? extends K> keyMapper, Function<? super T,? extends U> valueMapper, BinaryOperator<U> mergeFunction, Supplier<M> mapSupplier)
- static <T,K,U> Collector<T,?,Map<K,U>> toUnmodifiableMap(Function<? super T,? extends K> keyMapper, Function<? super T,? extends U> valueMapper)
- static <T,K,U> Collector<T,?,Map<K,U>> toUnmodifiableMap(Function<? super T,? extends K> keyMapper, Function<? super T,? extends U> valueMapper, BinaryOperator<U> mergeFunction) 10
- static <T,K,U> Collector<T,?,ConcurrentMap<K,U>> toConcurrentMap(Function<? super T,? extends K> keyMapper, Function<? super T,? extends U> valueMapper)
- static <T,K,U> Collector<T,?,ConcurrentMap<K,U>> toConcurrentMap(Function<? super T,? extends</li>
   K> keyMapper, Function<? super T,? extends U> valueMapper, BinaryOperator<U> mergeFunction)
- static <T,K,U,M extends ConcurrentMap<K,U>> Collector<T,?,M> toConcurrentMap(Function<? super T,? extends K> keyMapper, Function<? super T,? extends U> valueMapper, BinaryOperator<U> mergeFunction, Supplier<M> mapSupplier)

产生一个收集器,它会产生一个映射表,不可修改的映射表或并发映射表。keyMapper 和 valueMapper 函数会应用于每个收集到的元素上,从而在所产生的映射表中生成一个键/值项。默认情况下,当两个元素产生相同的键时,会抛出一个 IllegalStateException 异常。你可以提供一个 mergeFunction 来合并具有相同键的值。默认情况下,其结果是一个 HashMap 或 ConcurrentHashMap。你可以提供一个 mapSupplier,它会产生所期望的映射表实例。

# 1.10 群组和分区

在上一节中,你看到了如何收集给定国家的所有语言,但是其处理显得有些冗长。你必须为每个映射表的值都生成单例集,然后指定如何将现有值与新值合并。将具有相同特性的值群聚成组是非常常见的,因此 groupingBy 方法直接就支持它。

我们来看看通过国家聚成组 Locale 的问题。首先,构建该映射表:

Map<String, List<Locale>> countryToLocales = locales.collect(
 Collectors.groupingBy(Locale::getCountry));

函数 Locale::getCountry 是群组的分类函数 (classifier function), 你现在可以查找给定国家代码对应的所有 locale 了, 例如:

List<Locale> swissLocales = countryToLocales.get("CH");
// Yields locales de CH, fr CH, it CH and maybe more

注释:快速复习一下 locale:每个 locale都有一个语言代码(例如英语的 en)和一个国家代码(例如美国的 US)。locale en\_US 描述的是美国英语,而 en\_IE 是爱尔兰英语。某些国家有多个 locale。例如,ga\_IE 是爱尔兰的盖尔语,而前面的示例也展示了 JDK 知道瑞士至少有三个 locale。

当分类函数是谓词函数(即返回 boolean 值的函数)时,流的元素可以分为两个列表:该函数返回 true 的元素和其他的元素。在这种情况下,使用 partitioningBy 比使用 groupingBy 更高效。例如,在下面的代码中,我们将所有 locale 分成了使用英语和使用所有其他语言的两类:

Map<Boolean, List<Locale>> englishAndOtherLocales = locales.collect(
 Collectors.partitioningBy(l -> l.getLanguage().equals("en")));
List<Locale> englishLocales = englishAndOtherLocales.get(true);

直 注释:如果调用 groupingByConcurrent 方法,就会在使用并行流时获得一个被并行组装的并行映射表。这与 toConcurrentMap 方法完全类似。

# API java.util.stream.Collectors

- static <T,K> Collector<T,?,Map<K,List<T>>> groupingBy(Function<? super T,? extends K> classifier)
- static <T,K> Collector<T,?,ConcurrentMap<K,List<T> groupingByConcurrent(Function<? super T,? extends K> classifier)
   产生一个收集器,它会产生一个映射表或并发映射表,其键是将 classifier 应用于所有收集到的元素上所产生的结果,而值是由具有相同键的元素构成的一个个列表。
- static <T> Collector<T,?,Map<Boolean,List<T>>>> partitioningBy(Predicate<? super T> predicate) 产生一个收集器,它会产生一个映射表,其键是 true/false,而值是由满足 / 不满足谓词的元素构成的列表。

# 1.11 下游收集器

groupingBy 方法会产生一个映射表,它的每个值都是一个列表。如果想要以某种方式来处理这些列表,就需要提供一个"下游收集器"。例如,如果想要获得集而不是列表,那么可以使用上一节中看到的 Collectors.toSet 收集器:

Map<String, Set<Locale>> countryToLocaleSet = locales.collect(
 groupingBy(Locale::getCountry, toSet()));

直 注释: 在本节的这个示例以及后续示例中,我们认为静态导入java.util.stream Collectors.\*会使表达式更容易阅读。

Java 提供了多种可以将收集到的元素约简为数字的收集器:

• counting 会产生收集到的元素的个数。例如:

```
Map<String, Long> countryToLocaleCounts = locales.collect(
   groupingBy(Locale::getCountry, counting()));
```

可以对每个国家有多少个 locale 进行计数。

 summing(Int|Long|Double) 和 averaging(Int|Long|Double) 会接受一个函数作为引元,将 该函数应用到下游元素上,并产生它们的和或均值。例如:

```
public record City(String name, String state, int population) {}
. . .
Map<String, Integer> stateToCityPopulation = cities.collect(
    groupingBy(City::state, averagingInt(City::population)));
```

可以计算城市流中每个州的人口总和。

• maxBy 和 minBy 会接受一个比较器,并分别产生下游元素中的最大值和最小值。例如:

```
Map<String, Optional<City>> stateToLargestCity = cities.collect(
   groupingBy(City::state,
        maxBy(Comparator.comparing(City::population))));
```

可以产生每个州中人口最多的城市。

collectingAndThen 收集器在收集器后面添加了一个最终处理步骤。例如,如果我们想要知道有多少不同的结果,那么就可以将它们收集到一个集中,然后计算其尺寸:

```
Map<Character, Integer> stringCountsByStartingLetter = strings.collect(
  groupingBy(s -> s.charAt(0),
      collectingAndThen(toSet(), Set::size)));
```

mapping 收集器的做法正好相反,它会将一个函数应用于收集到的每个元素,并将结果传递给下游收集器。

```
Map<Character, Set<Integer>> stringLengthsByStartingLetter = strings.collect(
   groupingBy(s -> s.charAt(0),
```

这里,我们按照首字符对字符串进行了分组。在每个组内部,我们会计算字符串的长度,然后将这些长度收集到一个集中。

mapping 方法还针对上一节中的问题,即把某国所有的语言收集到一个集中,产生了一种更佳的解决方案。

```
Map<String, Set<String>> countryToLanguages = locales.collect(
   groupingBy(Locale::getDisplayCountry,
        mapping(Locale::getDisplayLanguage,
        toSet())));
```

还有一个 flatMapping 方法,可以与返回流的函数一起使用。

如果群组和映射函数的返回值为 int、long 或 double, 那么可以将元素收集到汇总统计对象中, 就像 1.8 节中所讨论的一样。例如,

```
Map<String, IntSummaryStatistics> stateToCityPopulationSummary = cities.collect(
   groupingBy(City::state,
        summarizingInt(City::population)));
```

然后,可以从每个组的汇总统计对象中获取这些函数值的总和、数量、平均值、最小值 和最大值。

filtering 收集器会将一个过滤器应用到每个组上,例如:

```
Map<String, Set<City>> largeCitiesByState
```

最后,你可以使用 teeing 收集器将其分解为两个并行的下游集合。当你需要在一个流中计算多个值时,它就会显得非常有用。假设我们想要收集城市名并计算它们的平均人口。虽然我们无法两次读取同一个流,但是 teeing 使得我们可以执行两次计算,此时只需指定两个下游收集器和将结果组合起来的函数。

```
record Pair<S, T>(S first, T second) {}
Pair<List<String>, Double> result = cities.filter(c -> c.state().equals("NV"))
   .collect(teeing(
        mapping(City::name, toList()), // First downstream collector
        averagingDouble(City::population), // Second downstream collector
        (list, avg) -> new Result(list, avg))); // Combining function
```

註释:还有3个版本的 reducing 方法,它们都应用了通用的约简操作,正如下一节中所描述的一样。

将收集器组合起来是一种很强大的方式,但是它也可能会导致产生非常复杂的表达式。 最佳用法是与 groupingBy 和 partitioningBy 一起处理 "下游的"映射表中的值。否则,应该 直接在流上应用诸如 map、reduce、count、max 或 min 这样的方法。

程序清单 1-6 中的示例程序演示了下游收集器。

#### 程序清单 1-6 collecting/DownstreamCollectors.java

```
package collecting;\nimport static java.util.stream.Collectors.*;\nimport java.io.*;\nimport java.nio.file.*;\nimport java.util.*;\nimport java.util.stream.*;

/**
```

```
* @author Cay Horstmann
12
13
14
  public class DownstreamCollectors
15
16
      public record City(String name, String state, int population) {}
17
      public static Stream<City> readCities(String filename) throws IOException
18
19
20
         return Files.lines(Path.of(filename))
            .map(l -> l.split(", "))
21
            .map(a -> new City(a[0], a[1], Integer.parseInt(a[2])));
23
24
      public static void main(String[] args) throws IOException
25
26
         Stream<Locale> locales = Stream.of(Locale.getAvailableLocales());
27
         Map<String, Set<Locale>> countryToLocaleSet = locales.collect(groupingBy(
28
            Locale::getCountry, toSet()));
         System.out.println("countryToLocaleSet: " + countryToLocaleSet);
38
31
         locales = Stream.of(Locale.getAvailableLocales());
32
         Map<String, Long> countryToLocaleCounts = locales.collect(groupingBy(
33
            Locale::getCountry, counting()));
34
         System.out.println("countryToLocaleCounts: " + countryToLocaleCounts);
35
36
         Stream<City> cities = readCities("cities.txt");
37
         Map<String, Integer> stateToCityPopulation = cities.collect(groupingBy(
            City::state, summingInt(City::population)));
39
         System.out.println("stateToCityPopulation: " + stateToCityPopulation);
48
41
         cities = readCities("cities.txt");
42
         Map<String, Optional<String>> stateToLongestCityName = cities
43
             .collect(groupingBy(City::state,
44
                mapping(City::name, maxBy(Comparator.comparing(String::length)))));
45
         System.out.println("stateToLongestCityName: " + stateToLongestCityName);
46
47
         locales = Stream.of(Locale.getAvailableLocales());
48
         Map<String, Set<String>> countryToLanguages = locales.collect(groupingBy(
49
            Locale::getDisplayCountry, mapping(Locale::getDisplayLanguage, toSet())));
50
         System.out.println("countryToLanguages: " + countryToLanguages);
51
         cities = readCities("cities.txt");
53
         Map<String, IntSummaryStatistics> stateToCityPopulationSummary = cities
54
             .collect(groupingBy(City::state, summarizingInt(City::population)));
55
         System.out.println(stateToCityPopulationSummary.get("NY"));
56
57
         cities = readCities("cities.txt");
58
         Map<String, String> stateToCityNames = cities.collect(groupingBy(
59
             City::state,
             reducing("", City::name, (s, t) \rightarrow s.length() == 0 ? t : s + ", " + t)));
61
62
         cities = readCities("cities.txt");
63
         stateToCityNames = cities.collect(groupingBy(City::state,
64
             mapping(City::name, joining(", "))));
         System.out.println("stateToCityNames: " + stateToCityNames);
66
```

```
67
         cities = readCities("cities.txt");
68
         record Pair<S, T>(S first, T second) {}
69
         Pair<List<String>, Double> result = cities.filter(c -> c.state().equals("NV"))
70
             .collect(teeing(
71
               mapping(City::name, toList()),
72
               averagingDouble(City::population),
73
               (names, avg) -> new Pair<>(names, avg)));
74
         System.out.println(result);
75
      }
76
77 }
```

#### API java.util.stream.Collectors

- public static <T,K,A,D> Collector<T,?,Map<K,D>> groupingBy(Function<? super T,? extends K> classifier, Collector<? super T,A,D> downstream)
   产生一个收集器,该收集器会产生一个映射表,其中的键是将 classifier 应用到所有收集到的元素上之后产生的结果,而值是使用下游收集器收集具有相同的键的元素所产生的结果。
- static <T> Collector<T,?,Long> counting()
   产生一个可以对收集到的元素进行计数的收集器。
- static <T> Collector<T,?,Integer> summingInt(ToIntFunction<? super T> mapper)
- static <T> Collector<T,?,Long> summingLong(ToLongFunction<? super T> mapper)
- static <T> Collector<T,?,Double> summingDouble(ToDoubleFunction<? super T> mapper) 产生一个收集器,对将 mapper 应用到收集到的元素上之后产生的结果计算总和。
- static <T> Collector<T,?,Optional<T>> maxBy(Comparator<? super T> comparator)
- static <T> Collector<T,?,Optional<T>> minBy(Comparator<? super T> comparator)
   产生一个收集器,使用 comparator 指定的排序方法,计算收集到的元素中的最大值和最小值。
- static <T,A,R,RR> Collector<T,A,RR> collectingAndThen(Collector<T,A,R> downstream, Function<R,RR> finisher)
  - 产生一个收集器,它会将元素发送到下游收集器中,然后将 finisher 函数应用到其结果上。
- static <T,U,A,R> Collector<T,?,R> mapping(Function<? super T,? extends U> mapper, Collector<? super U,A,R> downstream)
  - 产生一个收集器,它会在每个元素上调用 mapper,并将结果发送到下游收集器中。
- static <T,U,A,R> Collector<T,?,R> flatMapping(Function<? super T,? extends Stream<? extends</li>
   U>> mapper, Collector<? super U,A,R> downstream)
  - 产生一个收集器,它会在每个元素上调用 mapper,并将结果中的元素发送到下游收集器中。
- static <T,A,R> Collector<T,?,R> filtering(Predicate<? super T> predicate, Collector<? super T,A,R> downstream)
  - 产生一个收集器, 它会将满足谓词逻辑的元素发送到下游收集器中。

# 1.12 约简操作

reduce 方法是一种用于从流中计算某个值的通用机制,其最简单的形式将接受一个二元函数,并从前两个元素开始持续应用它。如果该函数是求和函数,那么就很容易解释这种机制:

```
List<Integer> values = . . .;
Optional<Integer> sum = values.stream().reduce((x, y) -> x + y);
```

在上面的情况中,reduce 方法会计算  $v_0+v_1+v_2+\cdots$ ,其中  $v_i$  是流中的元素。如果流为空,那么该方法会返回一个 0ptional,因为没有任何有效的结果。

直 注释: 在上面的情况中,可以写成 reduce(Integer::sum)而不是 reduce((x, y)→ x+y)。

更一般地,我们可以使用任何约简操作将部分结果 x 与下一个值 y 组合起来以产生新的部分结果。

下面是另一种看待约简的方式。给定约简操作 op,该约简会产生  $v_0$  op  $v_1$  op  $v_2$  op...,其中  $v_i$  op  $v_{i+1}$  表示函数调用  $op(v_i, v_{i+1})$ 。有很多种在实践中很有用的操作,例如求和、乘积、字符串连接、求最大值和最小值、求并集和交集等。

如果要用并行流来约简,那么这项约简操作必须是可结合的,即组合元素时使用的顺序不会产生任何影响。用数学标记法表示, $(x\ op\ y)\ op\ z$ 必须等于  $x\ op\ (y\ op\ z)$ 。减法是一个不可结合操作的例子,例如, $(6-3)-2\neq 6-(3-2)$ 。

通常,会有一个幺元值 e 使得 e op x=x,可以使用这个元素作为计算的起点。例如,0 是加法的幺元值。由此,我们可以使用第 2 种形式的 reduce:

```
List<Integer> values = . . .;
Integer sum = values.stream().reduce(\theta, (x, y) -> x + y);
// Computes \theta + v_{\theta} + v_{1} + v_{2} + . . .
```

如果流为空,则会返回幺元值,你就再也不需要处理 Optional 类了。

现在,假设你有一个对象流,并且想要对某些属性求和,例如字符串流中所有字符串的长度,那么你就不能使用简单形式的 reduce,而是需要 (T,T)->T 这样的函数,即引元和结果的类型相同的函数。但是在这种情况下,你有两种类型:流的元素具有 String 类型,而累积结果是整数。有一种形式的 reduce 可以处理这种情况。

首先,你需要提供一个"累积器"函数 (total, word) -> total + word.length()。这个函数会被反复调用,产生累积的总和。但是,当计算被并行化时,会有多个这种类型的计算,你需要将它们的结果合并。因此,你需要提供第二个函数来执行此处理。完整的调用如下:

```
int result = words.reduce(0,
  (total, word) -> total + word.length(),
  (total1, total2) -> total1 + total2);
```

註釋:在实践中,你可能并不会频繁地用到 reduce 方法。通常,映射为数字流并使用 其方法来计算总和、最大值和最小值会更容易。(我们将在 1.13 节中讨论数字流。)在 这个特定示例中,你可以调用 words.mapToInt(String::length).sum(),因为它不涉及装 箱操作,所以更简单也更高效。

- 注释:有时 reduce 会显得不够通用。例如,假设我们想要收集 BitSet 中的结果。如果收集操作是并行的,那么就不能直接将元素放到单个 BitSet 中,因为 BitSet 对象不是线程安全的。因此,我们不能使用 reduce,因为每个部分都需要以其自己的空集开始,并且 reduce 只能让我们提供一个幺元值。此时,应该使用具有 3 个引元形式的 collect,这些引元是:
  - 1. 一个提供者,它会创建目标对象的新实例。
  - 2. 一个累积器,它会将一个元素累加到该目标上。
  - 3. 一个组合器,它会将两个对象合并成一个。

下面的代码展示了 collect 方法是如何操作位集的:

BitSet result = stream.collect(BitSet::new, BitSet::set, BitSet::or);

#### API java.util.Stream 8

- Optional<T> reduce(BinaryOperator<T> accumulator)
- T reduce(T identity, BinaryOperator<T> accumulator)
- <U> U reduce(U identity, BiFunction<U,? super T,U> accumulator, BinaryOperator<U> combiner) 用给定的 accumulator 函数产生流中元素的累积总和。如果提供了幺元,那么第一个被累积的元素就是该幺元。如果提供了组合器,那么它可以用来将分别累积的各个部分整合成总和。
- <R> R collect(Supplier<R> supplier, BiConsumer<R,? super T> accumulator, BiConsumer<R,R> combiner)

将元素收集到类型 R 的结果中。在每个部分上,都会调用 supplier 来提供初始结果,调用 accumulator 来交替地将元素添加到结果中,并调用 combiner 来整合两个结果。

# 1.13 基本类型流

到目前为止,我们都是将整数收集到 Stream<Integer>中,尽管很明显,但是将每个整数都包装到包装器对象中却是很低效的。对其他基本类型来说,情况也是一样,这些基本类型是 double、float、long、short、char、byte 和 boolean。流库中具有专门的类型 IntStream、LongStream 和 DoubleStream,用来直接存储基本类型值,而无须使用包装器。如果想要存储 short、char、byte 和 boolean,可以使用 IntStream;而对于 float,可以使用 DoubleStream。

为了创建 IntStream, 需要调用 IntStream.of 和 Arrays.stream 方法:

IntStream stream = IntStream.of(1, 1, 2, 3, 5);
stream = Arrays.stream(values, from, to); // values is an int[] array

与对象流一样,我们还可以使用静态的 generate 和 iterate 方法。此外, IntStream 和 LongStream 有静态方法 range 和 rangeClosed,可以生成步长为 1 的整数范围:

IntStream zeroToNinetyNine = IntStream.range(0, 100); // Upper bound is excluded IntStream zeroToHundred = IntStream.rangeClosed(0, 100); // Upper bound is included

CharSequence 接口拥有 codePoints 和 chars 方法,可以生成由字符的 Unicode 码或由 UTF-16 编码机制的码元构成的 IntStream。

```
String sentence = "\uD835\uDD46 is the set of octonions."; 
 // \uD835\uDD46 is the UTF-16 encoding of the letter \mathbb O, unicode U+1D546
```

```
IntStream codes = sentence.codePoints();
// The stream with hex values 10546 20 69 73 20 . . .
```

当你有一个对象流时,可以用 mapToInt、mapToLong 或 mapToDouble 将其转换为基本类型流。例如,如果你有一个字符串流,并想将其长度处理为整数,那么就可以在 IntStream 中实现此目的:

```
Stream<String> words = . . .;
IntStream lengths = words.mapToInt(String::length);
```

为了将基本类型流转换为对象流,需要使用 boxed 方法:

Stream<Integer> integers = IntStream.range(0, 100).boxed();

通常,基本类型流上的方法与对象流上的方法类似。下面是主要的差异:

- toArray 方法会返回基本类型数组。
- 产生可选结果的方法会返回一个 OptionalInt、OptionalLong 或 OptionalDouble。这些类与 Optional 类类似,但是具有 getAsInt、getAsLong 和 getAsDouble 方法,而不是 get 方法。
- 具有分别返回总和、平均值、最大值和最小值的 sum、average、max 和 min 方法。对象 流没有定义这些方法。
- summaryStatistics 方法会产生一个类型为 IntSummaryStatistics、LongSummaryStatistics 或 DoubleSummaryStatistics 的对象,它们可以同时报告流的总和、数量、平均值、最大值和最小值。
- i 注释: Random 类具有 ints、longs 和 doubles 方法,它们会返回由随机数构成的基本类型流。如果需要的是并行流中的随机数,那么需要使用 SplittableRandom 类。

程序清单 1-7 给出了基本类型流的 API 的示例。

# 程序清单 1-7 streams/PrimitiveTypeStreams.java

```
package streams;
\nimport java.io.*;\nimport java.nio.file.*;\nimport java.util.stream.*;

/**
 * @version 1.02 2021-09-09
 * @author Cay Horstmann
 */
public class PrimitiveTypeStreams

public static void show(String title, IntStream stream)
```

```
{
14
         final int SIZE = 10;
15
         int[] firstElements = stream.limit(SIZE + 1).toArray();
16
         System.out.print(title + ": ");
17
          for (int i = 0; i < firstElements.length; i++)
18
19
             if (i > 0) System.out.print(", ");
28
             if (i < SIZE) System.out.print(firstElements[i]);</pre>
21
             else System.out.print("...");
22
23
          System.out.println();
24
25
26
      public static void main(String[] args) throws IOException
27
28
          IntStream is1 = IntStream.generate(() -> (int) (Math.random() * 100));
29
          show("is1", is1);
38
          IntStream is2 = IntStream.range(5, 10);
31
          show("is2", is2);
32
          IntStream is3 = IntStream.rangeClosed(5, 10);
33
          show("is3", is3);
34
35
          Path path = Path.of("../gutenberg/alice30.txt");
36
          var contents = Files.readString(path);
37
38
          Stream<String> words = Stream.of(contents.split("\\PL+"));
39
          IntStream is4 = words.mapToInt(String::length);
48
          show("is4", is4);
41
          String sentence = "\uD835\uDD46 is the set of octonions.";
42
43
          System.out.println(sentence);
          IntStream codes = sentence.codePoints();
AA
          System.out.println(codes.mapToObj(c -> "%X ".formatted(c)).collect(
45
             Collectors.joining()));
46
47
          Stream<Integer> integers = IntStream.range(0, 100).boxed();
48
          IntStream is5 = integers.mapToInt(Integer::intValue);
49
          show("is5", is5);
50
51
52 }
```

#### API java.util.stream.IntStream

- static IntStream range(int startInclusive, int endExclusive)
- static IntStream rangeClosed(int startInclusive, int endInclusive)
   产生一个由给定范围内的整数构成的 IntStream。
- static IntStream of(int... values) 产生一个由给定元素构成的 IntStream。
- int[] toArray() 产生一个由当前流中的元素构成的数组。
- int sum()

- OptionalDouble average()
- OptionalInt max()
- OptionalInt min()
- IntSummaryStatistics summaryStatistics()
   产生当前流中元素的总和、平均值、最大值和最小值,或者产生一个可以从中获取所有这四个值的对象。
- Stream<Integer> boxed()产生用于当前流中的元素的包装器对象流。

#### API java.util.stream.LongStream

- static LongStream range(long startInclusive, long endExclusive)
- static LongStream rangeClosed(long startInclusive, long endInclusive)
   用给定范围内的整数产生一个 LongStream。
- static LongStream of(long... values)
   用给定元素产生一个 LongStream。
- long[] toArray()用当前流中的元素产生一个数组。
- long sum()
- OptionalDouble average()
- OptionalLong max()
- OptionalLong min()
- LongSummaryStatistics summaryStatistics()
   产生当前流中元素的总和、平均值、最大值和最小值,或者产生一个可以从中获取所有这四个值的对象。
- Stream<Long> boxed()产生用于当前流中的元素的包装器对象流。

# API java.util.stream.DoubleStream 8

- static DoubleStream of(double... values)
   用给定元素产生一个 DoubleStream。
- double[] toArray()用当前流中的元素产生一个数组。
- double sum()
- OptionalDouble average()
- OptionalDouble max()
- OptionalDouble min()
- DoubleSummaryStatistics summaryStatistics()

产生当前流中元素的总和、平均值、最大值和最小值,或者产生一个可以从中获取所有这四个值的对象。

Stream<Double> boxed()产生用于当前流中的元素的包装器对象流。

#### API java.lang.CharSequence

IntStream codePoints() 8
 产生由当前字符串的所有 Unicode 码点构成的流。

#### API java.util.random.RandomGenerator

- IntStream ints()
- IntStream ints(int randomNumberOrigin, int randomNumberBound)
- IntStream ints(long streamSize)
- IntStream ints(long streamSize, int randomNumberOrigin, int randomNumberBound)
- LongStream longs()
- LongStream longs(long randomNumberOrigin, long randomNumberBound)
- LongStream longs(long streamSize)
- LongStream longs(long streamSize, long randomNumberOrigin, long randomNumberBound)
- DoubleStream doubles()
- DoubleStream doubles(double randomNumberOrigin, double randomNumberBound)
- DoubleStream doubles(long streamSize)
- DoubleStream doubles(long streamSize, double randomNumberOrigin, double randomNumberBound) 产生随机数流。如果提供了 streamSize, 这个流就是具有给定数量元素的有限流。当 提供了边界时,其元素将位于 randomNumberOrigin (包含) 和 randomNumberBound (不包含)的区间内。

# API java.util.Optional(Int|Long|Double)

- static Optional(Int|Long|Double) of((int|long|double) value)
   用所提供的基本类型值产生一个可选对象。
- (int|long|double) getAs(Int|Long|Double)() 产生当前可选对象的值,或者在其为空时抛出一个 NoSuchElementException 异常。
- (int|long|double) orElse((int|long|double) other)
- (int|long|double) or Else Get((Int|Long|Double) Supplier other) 产生当前可选对象的值,或者在这个对象为空时产生可替代的值。
- void ifPresent((Int|Long|Double)Consumer consumer)
   如果当前可选对象不为空,则将其值传递给 consumer。

# api java.util.(Int|Long|Double)SummaryStatistics

long getCount()

- (int|long|double) getSum()
- double getAverage()
- (int|long|double) getMax()
- (int | long | double) getMin() 产生收集到的元素的数量、总和、平均值、最大值和最小值。

# 1.14 并行流

流使并行处理块操作变得很容易。这个过程几乎是自动的,但是需要遵守一些规则。首先,必须有一个并行流。可以用 Collection.parallelStream() 方法从任何集合中获取一个并行流:

Stream<String> parallelWords = words.parallelStream();

而且, parallel 方法可以将任意的顺序流转换为并行流。

Stream<String> parallelWords = Stream.of(wordArray).parallel();

只要在终结方法执行时流处于并行模式, 所有的中间流操作就都将被并行化。

当流操作并行运行时,目标是让其返回结果与顺序执行时返回的结果相同。重要的是, 这些操作是无状态的,并且可以以任意顺序执行。

下面的示例是一项你无法完成的任务。假设你想要对字符串流中的所有短单词计数:

```
var shortWords = new int[12];
words.parallelStream().forEach(
   s -> { if (s.length() < 12) shortWords[s.length()]++; });
      // ERROR--race condition!
System.out.println(Arrays.toString(shortWords));</pre>
```

这是一种非常糟糕的代码。传递给 forEach 的函数会在多个并发线程中运行,每个都会更新共享的数组。正如我们在卷 I 第 12 章中所解释的,这是一种经典的竞争情况。如果多次运行这个程序,你很可能就会发现每次运行都产生不同的计数值,而且每个都是错的。

你的职责是确保传递给并行流操作的任何函数都可以安全地并行执行,达到这个目的的 最佳方式是远离可修改状态。在本例中,如果用长度将字符串分组,然后分别对它们进行计 数,那么就可以安全地并行化这项计算。

```
Map<Integer, Long> shortWordCounts
```

默认情况下,从有序集合(数组和列表)、范围、生成器和迭代器产生的流,或者通过调用 Stream.sorted 产生的流,都是有序的。它们的结果是按照原来元素的顺序累积的,因此是完全可预知的。如果运行相同的操作两次,将会得到完全相同的结果。

排序并不排斥高效的并行处理。例如,当计算 stream.map(fun) 时,流可以被划分为n 部分,它们会被并行地处理。然后,结果将会按照顺序重新组装起来。

当放弃排序需求时,有些操作可以被更有效地并行化。通过在流上调用 Stream.unor-dered 方法,就可以明确表示我们对排序不感兴趣。Stream.distinct 就是从这种方式中获益的一种操作。在有序的流中,distinct 会保留所有相同元素中的第一个,这对并行化是一种阻碍,因为处理每个部分的线程在其之前的所有部分都被处理完之前,并不知道应该丢弃哪些元素。如果可以接受保留唯一元素中任意一个的做法,那么所有部分就可以并行地处理(使用共享的集合来跟踪重复元素)。

还可以通过放弃排序要求来提高 limit 方法的速度。如果只想从流中取出任意 n 个元素,而并不在意到底要获取哪些,那么可以调用:

Stream<String> sample = words.parallelStream().unordered().limit(n);

正如 1.9 节所讨论的,合并映射表的代价很高昂。正是这个原因,Collectors.grouping-ByConcurrent 方法使用了共享的并发映射表。为了从并行化中获益,映射表中值的顺序不会与流中的顺序相同。

```
Map<Integer, List<String>> result = words.parallelStream().collect(
   Collectors.groupingByConcurrent(String::length));
   // Values aren't collected in stream order
```

当然,如果使用独立于排序的下游收集器,那么就不必在意了,例如:

```
Map<Integer, Long> wordCounts
```

不要指望将所有的流都转换为并行流就能够加速操作,要牢记下面几条:

- 并行化会导致大量的开销,只有面对非常大的数据集才划算。
- 只有在底层的数据源可以被有效地分割为多个部分时,将流并行化才有意义。
- 并行流使用的线程池可能会因诸如文件 I/O 或网络访问这样的操作被阻塞而饿死。 只有在面对海量的内存数据和运算密集的处理时,并行流才会发挥出最大的功效。
- √ 提示:在 Java 9 之前,对 Files.lines 方法返回的流进行并行化是没有意义的。因为数据是不可分割的,所以我们只能在读取文件的后半部分之前读取前半部分。现在,该方法使用的是内存映射文件,因此可以有效地进行分割。如果想要处理一个大型文件的各个行,并行化这个流可能会提高性能。
- **注释**: 默认情况下,并行流使用的是 ForkJoinPool.commonPool 返回的全局 fork-join 池。只有在操作不会阻塞并且我们不会将这个池与其他任务共享的情况下,这种方式才不会有什么问题。有一种解决方法是使用另一个不同的池,即把操作放置到定制的池的 submit 方法中:

```
ForkJoinPool customPool = . . .;
result = customPool.submit(() ->
    stream.parallel().map(. . .).collect(. . .)).get();

或者,使用异步方式:

CompletableFuture.supplyAsync(() ->
    stream.parallel().map(. . .).collect(. . .),
    customPool).thenAccept(result -> . . .);
```

直 注释: 如果想要并行化基于随机数的流计算,那么请不要以从 Random.ints、Random. longs 或 Random.doubles 方法中获得的流为起点,因为这些流不可分割。应该使用 SplittableRandom 类的 ints、longs 或 doubles。

程序清单 1-8 中的示例程序展示了如何操作并行流。

#### 程序清单 1-8 parallel/ParallelStreams.java

```
package parallel;
2
  import static java.util.stream.Collectors.*;
5 import java.io.*;
6 import java.nio.file.*;
7 import java.util.*;
  import java.util.stream.*;
9
18
   * @version 1.02 2019-08-28
11
   * @author Cay Horstmann
12
13
   public class ParallelStreams
14
   {
15
      public static void main(String[] args) throws IOException
16
17
         var contents = Files.readString(
18
            Path.of("../gutenberg/alice30.txt"));
19
28
         List<String> wordList = List.of(contents.split("\\PL+"));
21
         // Very bad code ahead
22
         var shortWords = new int[1θ];
23
         wordList.parallelStream().forEach(s ->
24
25
               if (s.length() < 10) shortWords[s.length()]++;
26
            1):
27
         System.out.println(Arrays.toString(shortWords));
28
29
         // Try again--the result will likely be different (and also wrong)
38
         Arrays.fill(shortWords, 0);
31
         wordList.parallelStream().forEach(s ->
32
33
               if (s.length() < 10) shortWords[s.length()]++;
34
            });
35
```

```
System.out.println(Arrays.toString(shortWords));
36
37
         // Remedy: Group and count
38
         Map<Integer, Long> shortWordCounts = wordList.parallelStream()
39
             .filter(s \rightarrow s.length() < 10)
48
            .collect(groupingBy(String::length, counting()));
41
47
         System.out.println(shortWordCounts);
43
44
         // Downstream order not deterministic
45
         Map<Integer, List<String>> result = wordList.parallelStream().collect(
46
            Collectors.groupingByConcurrent(String::length));
47
48
         System.out.println(result.get(14));
49
5θ
         result = wordList.parallelStream().collect(
51
            Collectors.groupingByConcurrent(String::length));
52
53
         System.out.println(result.get(14));
54
55
         Map<Integer, Long> wordCounts = wordList.parallelStream().collect(
            groupingByConcurrent(String::length, counting()));
57
58
         System.out.println(wordCounts);
59
60
61 }
```

## para.util.stream.BaseStream<T,S extends BaseStream<T,S>>

- S parallel()

  产生一个与当前流中元素相同的并行流。
- \$ unordered() 产生一个与当前流中元素相同的无序流。

# API java.util.Collection<E>

• Stream<E> parallelStream() 8 用当前集合中的元素产生一个并行流。

在本章中, 你学习到了如何运用 Java 8 的流库。下一章将讨论另一个重要的主题:输入与输出。

# *2 入与 出*

- *人/ 出流*
- *写二 制数据*
- *对象输入/ 出流与序列化*
- *操作文件*

- *内存映射文件*
- *文件加 机制*
- *正则表达式*

*本 将介 Java中 于 人和 出 各 应用编程接口 Application Programming Interface, API <sup>O</sup>你将 学习如何 文件与 <sup>录</sup> 以及如何以二 制格式和文本格式来 写数据。本章还要向你展 对 序列化机制 它可以使存储对 像存储文本和数值数据一样 容易。然后 我们将介 如何使 文件和 录。最后 本 将讨论正则表达式 尽管这部分 内容实 上与 入和 出并不 关 但是我们 实也找不到更合 地方来处 个 。 很明显 Java 团 在 个 处 上和我们一样 因为正则 式AH 格 明 属于"新I/O" <sup>性</sup> <sup>格</sup> <sup>明</sup>。*

# *2.1 <sup>入</sup>/ 出流*

*在Java API中 可以从其中 人一个字 序列 对 作 入流 可以向其中写人一 个字 序列 对 作 出流。 些字 序列 来源地和 地可以是文件 且 常就是 文件 但是也可以是网络连接 是内存块。抽 InputStream和Outputstream构成了 入/ 出 I/O 层次 构 基 。*

*注 些 入/ 出流与在前一 中 到 流没有任何关 。为了清楚 只 是 于 入和檢出 流 我们 将使 术 入流、 出流或 入/ 出流。 a*

*因为 向字 入/ 出流不便于处 以Unicode形式存储 信息 回忆一下 Unicode中每个字符都使 了多个字 来表示 所以从抽 Reader和Writer中 承出来了 一个专 于处 Unicode字 单 层次 构。 些 拥有 入和写出操作 是基 于两字节的Char值 即Unicode 元 不是基于byte值 。*

# *2.1.1 写字*

*I<sup>叩</sup>utSt ream 有一个抽 方法*

*abstract int read*

*个方法将 入一个字 并 回 入 字 或 在 到 入源 尾时 回-1。在 具体的输人流 时 了 个方法以提供 功 例如 在Fileinput St ream* *<sup>中</sup> 个方法将从某个文件中 人一个字 System.in (它是InputStream 一个子 定义对 )却是从"标准 人"中 人信息 即从控制台或 定向 文件中 人信息。*

*InputStream 有 干个 抽 方法 它们可以 人一个字 数 或者跳过大量的 字 。从Java 9开始 有了一个 常有 可以 取流中所有字 方法*

```
byte[】bytes = in.readAUBytesO;
```

*有多个 来 取 定数 字 方法 可以参 API 明。*

*些方法 抽 read方法 因此 各个子类都只需覆盖这一个方法。*

*与此 似 OutputStream 定义了下 抽 方法*

```
abstract void write(int b)
```

*它可以向某个 出位 写出一个字 。*

*如果我们有一个字 数 么就可以一次性地写出它们*

```
byte[] values =...;
out.write(values); .
```

*transferTo方法可以将所有字 从一个 人流传 到一个 出流*

```
in.transferTo(out);
```

*read和write方法在执 时 将 塞 字 实 人或写出。 就意味 如果流 不 即 ( 常是因为 接忙) 么当前 将 塞。 使得在 两个方法 待指定 流变为可 段时 其他的线程就有机会去执 有用的工作。*

*available方法使我们可以去检査当前可 入 字 数 意味 像下 样 代 段不可 塞*

```
int bytesAvailable = in.available!);
if (bytesAvailable > 8)
{
   var data = new byte[bytesAvailable];
   in.read(data);
}
```

*当你完成对 人/ 出流 写时 应该通过调用dose方法来关 它 个 会 放掉十分有 操作 源。如果一个应 序打开了 多 人/ 出流 没有关 , 么系统资源将被耗尽。关 一个 出流 同时 会冲刷 于 出流 冲区 所有 临 时 于 冲区中 以便 更大 包 形式传 字 在关 出流时 将 出。 别是, 如果不关 文件 么写出字 最后一个包可 永 也得不到传 。当然 我们 可以 flush方法来人为地冲刷 些 出。*

*即使某个 入/ 出流 提供了使 原 read和write功 某些具体方法 应 序员 是彳 少使 它们 因为大家感兴 数据可 包含数字、字 串和对 不是原 字 。*

*我们可以使 众多 构建于基本 InputStream和OutputStream 之上 某个 人/ 出 不只是 接使 字 。*

# *Awj java.io.InputStream*

*• abstract int read()*

从数据中读入一个字节,并返回该字节。这个 read 方法在碰到输入流的结尾时返回 -1。

• int read(byte[] b)

读人一个字节数组,并返回实际读入的字节数,或者在碰到输入流的结尾时返回 -1。 这个 read 方法最多读入 b. length 个字节。

- int read(byte[] b, int off, int len)
- int readNBytes(byte[] b, int off, int len) 9
   如果未阻塞(read),则读入由 len 指定数量的字节,或者阻塞至所有的值都被读入(readNBytes)。读入的值将置于 b 中从 off 开始的位置。返回实际读入的字节数,或者在碰到输入流的结尾时返回 -1。
- byte[] readAllBytes() 9产生一个数组,包含可以从当前流中读入的所有字节。
- long transferTo(OutputStream out)
   将当前输入流中的所有字节传送到给定的输出流,返回传递的字节数。这两个流都不 应该处于关闭状态。
- long skip(long n) 尝试在输入流中跳过 n 个字节,返回实际跳过的字节数(出于某种原因,可能会小于 n)。
- long skipNBytes(long n) 12
   在输入流中跳过 n 个字节,返回实际跳过的字节数(如果碰到输入流的结尾,则可能小于 n)。
- int available()
   返回在不阻塞的情况下可获取的字节数(回忆一下,阻塞意味着当前线程将失去它对资源的占用)。
- void close()关闭这个输入流。
- void mark(int readlimit)
   在输入流的当前位置打一个标记(并非所有的流都支持这个特性)。如果从输入流中已经读入的字节多于 readlimit 个,则这个流允许忽略这个标记。
- void reset()
   返回到最后一个标记,随后对 read 的调用将重新读入这些字节。如果当前没有任何标记,则这个流不被重置。
- boolean markSupported()
   如果这个流支持打标记,则返回 true。
- static InputStream nullInputStream() 11 返回一个不包含任何字节的输入流。

# API java.io.OutputStream 1.0

- abstract void write(int n)写出一个字节的数据。
- void write(byte[] b)

- void write(byte[] b, int off, int len) 写出所有字节或者某个范围的字节到数组 b 中。
- void close()冲刷并关闭输出流。
- void flush()冲刷输出流,也就是将所有缓冲的数据发送到目的地。
- static OutputStream nullOutputStream() 11
   返回一个会丢弃所有字节的输出流。

#### 2.1.2 完整的流家族

与 C 语言只有单一类型 FILE\* 包打天下不同, Java 拥有一个流家族, 包含各种输入/输出流类型, 其数量超过 60 个! 请参见图 2-1 和图 2-2。

![](_page_59_Figure_8.jpeg)

图 2-1 输入流与输出流的层次结构

![](_page_60_Figure_2.jpeg)

图 2-2 Reader 和 Writer 的层次结构

让我们把输入/输出流家族中的成员按照它们的使用方法来进行划分,这样就形成了处理字节和字符的两个单独的层次结构。正如所见,InputStream 和 OutputStream 类可以读写单个字节或字节数组,这些类构成了图 2-1 所示的层次结构的基础。要想读写字符串和数字,就需要功能更强大的子类,例如,DataInputStream 和 DataOutputStream 可以以二进制格式读写所有的基本 Java 类型。最后,还包含了多个很有用的输入/输出流,例如,ZipInputStream 和 ZipOutputStream 可以读写常见的 ZIP 压缩格式的文件。

另一方面,对于 Unicode 文本,可以使用抽象类 Reader 和 Writer 的子类 (请参见图 2-2)。 Reader 和 Writer 类的基本方法与 InputStream 和 OutputStream 中的方法类似。

abstract int read()
abstract void write(int c)

read 方法将返回一个 UTF-16 码元 (一个在 0~65535 之间的整数),或者在碰到文件结

尾时返回 -1。write 方法在被调用时,需要传递一个 Unicode 码元(请查看卷 I 第 3 章有关 Unicode 码元的讨论)。

还有 4 个 附加的接口: Closeable、Flushable、Readable 和 Appendable (请查看图 2-3)。 前两个接口非常简单,它们分别拥有下面的方法:

void close() throws IOException

和

void flush()

![](_page_61_Picture_7.jpeg)

图 2-3 Closeable、Flushable、Readable 和 Appendable 接口

InputStream、OutputStream、Reader和Writer都实现了Closeable接口。

**注释**: java.io.Closeable 接口扩展了 java.lang.AutoCloseable 接口。因此,对任何 Closeable 进行操作时,都可以使用 try-with-resource 语句<sup>⑤</sup>。为什么要有两个接口呢? 因为 Closeable 接口的 close 方法只抛出 IOException,而 AutoCloseable.close 方法可以抛出任何异常。

而 OutputStream 和 Writer 还实现了 Flushable 接口。

<sup>○</sup> try-with-resource 语句是指声明了一个或多个资源的 try 语句。——译者注

# *Readable接口只有一个方法:*

*int read(CharBuffer cb)*

*CharBuffer 拥有按 序和 机地 写 方法 它 一个内存中 冲区或 一个内存映像 文件( 参 2.5.2 以了 )。*

*Appendable接口有两个 于添加单个字 和字 序列 方法*

*Appendable append(char c) Appendable append(CharSequence s)*

*CharSequence接口描 了一个 char值序列 基本属性 String. CharBuffer、StringBuilder 和StringBuffer 实 了它。*

*在流 家族中 只有Writer实 了 Appendable。*

#### *j java.io.Closeable*

*• void closed 关闭这个Closeable 个方法可 会抛出IOException。*

## *ar] java.io.Flushable*

*• void flush() 冲刷 个Flushable。*

#### *r ah<sup>|</sup> java.lang.Readable*

*• int read(CharBuffer cb) 尝 向cb 人其可持有数 char值。 回 人 cha「值 数 或 当从 个 Readable中无法再 得更多 值时 回-1。*

# *ah] java.lang.Appendable*

- *• Appendable append(char c)*
- *• Appendable append(CharSequence cs) 向 个Appendable中 加 定 元或 定 序列中 所有 元 回this。*

# *ah<sup>|</sup> java.lang.CharSequence*

- *• char charAt(int index) 回 定 引处的码元。*
- *• int length() 回在 个序列中的码元 数 。*
- *• CharSequence subSequence(int startindex, int endindex) 回 存储在startindex到endindex-1处 所有 元构成 CharSequence。*
- *• String toStringO 回 个序列中所有 元构成 字 串。*

#### 2.1.3 组合输入/输出流过滤器

FileInputStream 和 FileOutputStream 可以提供附着在一个磁盘文件上的输入流和输出流,而你只需向其构造器提供文件名或文件的完整路径名。例如:

var fin = new FileInputStream("employee.dat");

这行代码可以查看用户目录下名为 "employee.dat"的文件。

- ☑ 提示: 所有在 java.io 中的类都将相对路径名解释为以用户工作目录开始,你可以通过调用 System.getProperty("user.dir")来获得这个信息。
- 警告:由于反斜杠字符在 Java 字符串中是转义字符,因此要确保在 Windows 风格的路径名中使用 \\ (例如, C:\\Windows\\win.ini)。在 Windows 中,还可以使用单斜杠字符(C:/\Windows/\win.ini),因为大部分 Windows 文件处理的系统调用都会将斜杠解释成文件分隔符。但是,并不推荐这样做,因为 Windows 系统函数的行为会因与时俱进而发生变化。因此,对于可移植的程序来说,应该使用程序所运行平台的文件分隔符,我们可以通过常量字符串 java.io.File.separator 获得它。

与抽象类 InputStream 和 OutputStream 一样,这些类只支持在字节级别上的读写。也就是说,我们只能从 fin 对象中读入字节和字节数组。

```
byte b = (byte) fin.read();
```

正如下节中看到的,如果我们只有 DataInputStream,那么我们就只能读人数值类型:

```
DataInputStream din = . . .;
double x = din.readDouble();
```

但是正如 FileInputStream 没有任何读入数值类型的方法一样,DataInputStream 也没有任何从文件中获取数据的方法。

Java 使用了一种灵巧的机制来分离这两种职责。某些输入流(例如 FileInputStream 和由 URL 类的 openStream 方法返回的输入流)可以从文件和其他更外部的位置上获取字节,而其他的输入流(例如 DataInputStream)可以将字节组装到更有用的数据类型中。Java 程序员必须对二者进行组合。例如,为了从文件中读入数字,首先需要创建一个 FileInputStream,然后将其传递给 DataInputStream 的构造器:

```
var fin = new FileInputStream("employee.dat");
var din = new DataInputStream(fin);
double x = din.readDouble();
```

如果再次查看图 2-1, 你就会看到 FilterInputStream 和 FilterOutputStream 类。这些类的子类用于向处理字节的输入/输出流添加额外的功能。

你可以通过嵌套过滤器来添加多重功能。例如,输入流在默认情况下是不被缓冲区缓存的,也就是说,每个对 read 的调用都会请求操作系统再分发一个字节。相比之下,请求一个数据块并将其置于缓冲区中会显得更加高效。如果我们想使用缓冲机制和用于文件的数据输

人方法,那么就需要使用下面这种相当复杂的构造器序列:

```
var din = new DataInputStream(
   new BufferedInputStream(
        new FileInputStream("employee.dat")));
```

注意,我们把 DataInputStream 置于构造器链的最后,这是因为我们希望使用 DataInput-Stream 的方法,并且希望它们能够使用带缓冲机制的 read 方法。

有时当多个输入流链接在一起时,你需要跟踪各个中介输入流(intermediate input stream)。例如,当读入输入时,你经常需要预览下一个字节,以了解它是否是你想要的值。Java 提供了用于此目的的 PushbackInputStream:

```
var pbin = new PushbackInputStream(
   new BufferedInputStream(
        new FileInputStream("employee.dat")));
```

现在你可以预读下一个字节:

int b = pbin.read();

并且在它并非你所期望的值时将其推回流中。

if (b != '<') pbin.unread(b);

但是读入和推回是可应用于可回推(pushback)输入流的仅有的方法。如果你希望能够 预先浏览并且还可以读入数字,那么就需要一个既是可回推输入流,又是一个数据输入流的 引用。

```
var pbin = new PushbackInputStream(
   new BufferedInputStream(
        new FileInputStream("employee.dat")));
var din = new DataInputStream(pbin);
```

当然,在其他编程语言的输入/输出流类库中,诸如缓冲机制和预览等细节都是自动处理的。因此,相比较而言,Java就有一点麻烦,它必须将多个流过滤器组合起来。但是,这种混合并匹配过滤器类以构建真正有用的输入/输出流序列的能力,将带来极大的灵活性,例如,你可以从一个ZIP压缩文件中通过使用下面的输入流序列来读入数字(请参见图 2-4):

```
var zin = new ZipInputStream(new FileInputStream("employee.zip"));
var din = new DataInputStream(zin);
```

(请查看 2.3.3 节以了解更多有关 Java 处理 ZIP 文件功能的知识。)

# API java.io.FileInputStream 1.0

- FileInputStream(String name)
- FileInputStream(File file)

使用由 name 字符串或 file 对象指定路径名的文件创建一个新的文件输入流(File 类在本章结尾处描述)。非绝对的路径名将按照相对于 VM 启动时所设置的工作目录来解析。

![](_page_65_Picture_2.jpeg)

*图2-4 滤器流序列*

# *<sup>a</sup>«] java. io. FileOutputStreu*

- *• FileOutputSt ream(String name)*
- *• <sup>F</sup>ileOutputSt ream(String name, boolean append)*
- *• FileOutputStream(File file)*
- *• FileOutputStream(File file, boolean append) <sup>使</sup> name<sup>字</sup> 串或file<sup>对</sup> 指定 径名 文件创建一个新 文件 出流(File <sup>在</sup> 本 尾处描 )。如果append参数为true, 么数据将 添加到文件尾 具有 同名字 已有文件不会 删 否则 个方法会删 所有具有 同名字 已有文件。*

# *ar! java.io.BufferedlnputStream*

*• BufferedlnputStream(I<sup>叩</sup>utStream in) 创建一个带 冲区 人流。带 冲区 人流在从流中 入字 时 不会每次 产 一次 备 操作。当 冲区为 时 会向 冲区中 人一个新 数据块。*

# *<sup>w</sup>j<sup>j</sup>ava.io.BufferedOutputStream*

*• Buffe redOutputSt ream(OutputSt ream out) 创建一个带 冲区 出流。带 冲区 出流在收 写出 字 时 不会每次 产 一次 备 操作。当 冲区填满或当流 冲刷时 数据就 写出。*

# *ah java.io.PushbacklnputStream*

- *• PushbackInputStream(I叩utStream in)*
- *• PushbacklnputStream(InputStream in, int size) 构建一个可以 一个字 或 具有指定尺寸 回推 冲区 入流。*
- *• void unread(int b) 回推一个字 它可以在下次调用read时 再次 取。*

#### 2.1.4 文本输入与输出

在保存数据时,可以选择二进制格式或文本格式。例如,整数 1234 存储成二进制数时,会被写为由字节 00 00 04 D2 构成的序列(十六进制表示法),而存储成文本格式时,则被存成了字符串"1234"。尽管二进制格式的 I/O 高速且高效,但是不适合人类阅读。我们首先讨论文本格式的 I/O,然后在 2.2 节中讨论二进制格式的 I/O。

在存储文本字符串时,需要考虑字符编码(character encoding)方式。在 Java 内部使用的 UTF-16 编码方式中,字符串"José"编码为 00 4A 00 6F 00 73 00 E9 (十六进制)。但是,许多程序都 希望文本文件按照其他的编码方式编码。在 UTF-8 这种在互联网上最常用的编码方式中,这个字符串将写出为 4A 6F 73 C3 A9,其中前 3 个字母无须补齐任何全 0 字节,而字符 é 占用了两个字节。

OutputStreamWriter 类将使用选定的字符编码方式,把 Unicode 码元的输出流转换为字节流。而 InputStreamReader 类将包含字节 (用某种字符编码方式表示的字符) 的输入流转换为可以产生 Unicode 码元的读入器。

例如,下面的代码就展示了如何让输入读入器从控制台读入键盘敲击信息,并将其转换为 Unicode:

var in = new InputStreamReader(System.in);

这个输入流读人器会假定使用主机系统所使用的默认字符编码方式。在桌面操作系统中,它可能是像 Windows 1252 或 MacRoman 这样古老的字符编码方式。你应该总是在 InputStreamReader 的构造器中选择一种具体的编码方式。例如,

var in = new InputStreamReader(new FileInputStream("data.txt"), StandardCharsets.UTF\_8);

请查看 2.1.8 节以了解字符编码方式的更多信息。

Reader 和 Writer 类都只有读人和写出单个字符的基础方法。在使用流时,可以使用处理字符串和数字的子类。

# 2.1.5 如何写出文本输出

对于文本输出,可以使用 PrintWriter。这个类拥有以文本格式打印字符串和数字的方法。为了打印文件,需要用文件名和字符编码方式构建一个 PrintStream 对象:

var out = new PrintWriter("employee.txt", StandardCharsets.UTF\_8);

为了输出到打印写出器,需要使用与使用 System.out 时相同的 print、println 和 printf 方法。你可以用这些方法来打印数字(int、short、long、float、double)、字符、boolean 值、字符串和对象。

例如,考虑下面的代码:

String name = "Harry Hacker";
double salary = 75000;
out.print(name);
out.print(' ');
out.println(salary);

它将把字符

Harry Hacker 75000.0

输出到写出器 out, 之后这些字符将会被转换成字节并最终写入 employee.txt 中。

println 方法在行中添加了对目标系统来说恰当的行结束符(Windows 系统是 "\r\n", UNIX 系统是 "\n"), 也就是通过调用 System.getProperty("line.separator") 而获得的字符串。

如果写出器设置为自动冲刷模式,那么只要 println 被调用,缓冲区中的所有字符都会 被发送到它们的目的地(打印写出器总是带缓冲区的)。默认情况下,自动冲刷机制是禁用的, 你可以通过使用 PrintWriter(Writer writer, boolean autoFlush) 来启用或禁用自动冲刷机制:

var out = new PrintWriter( new OutputStreamWriter( new FileOutputStream("employee.txt"), StandardCharsets.UTF 8), true); // autoflush

print 方法不抛出异常, 你可以调用 checkError 方法来查看输出流是否出现了某些错误。

■ 注释: Java 的老手们可能会很想知道 PrintStream 类和 System.out 到底怎么了。在 Java 1.0 中, PrintStream 类只是通过将高字节丢弃的方式把所有 Unicode 字符截断成 ASCII 字符。(那时, Unicode 仍旧是 16 位编码方式。) 很明显, 这并非一种干净利落和可移 植的方式,这个问题在 Java 1.1 中通过引入读入器和写出器得到了修正。为了与已有 的代码兼容, System.in、System.out 和 System.err 仍旧是输入/输出流而不是读入器和 写出器。但是现在 PrintStream 类在内部采用与 PrintWriter 相同的方式将 Unicode 字 符转换成了默认的主机编码方式。当你在使用 print 和 println 方法时, PrintStream 类 型的对象的行为看起来确实很像打印写出器,但是与打印写出器不同的是,它们允许 用 write(int) 和 write(byte[]) 方法输出原生字节。

# API java.io.PrintWriter

- PrintWriter(Writer out)
- PrintWriter(Writer writer) 创建一个向给定的写出器写出的新的 PrintWriter。
- PrintWriter(String filename, String encoding)
- PrintWriter(File file, String encoding) 创建一个使用给定的编码方式向给定的文件写出的新的 PrintWriter。
- void print(Object obj) 通过打印从 toString 产生的字符串来打印一个对象。
- void print(String s) 打印一个包含 Unicode 码元的字符串。
- void println(String s) 打印一个字符串,后面紧跟一个行终止符。如果这个流处于自动冲刷模式,那么就会 冲刷这个流。

- *• void print(char[] s) 打印在 定 字 串中 所有Unicode 元。*
- *• void print(char c) 打印一个Unicode 元。*
- *• void print(int i)*
- *• void print(long I)*
- *• void print(float f)*
- *• void print(double d)*
- *• void print(boolean b) 以文本格式打印 定 值。*
- *• void printf(String format, Object.., args) 按照格式字 串指定 方式打印 定 值。 査 卷1 3 以了 格式字 串 关 。*
- *• boolean checkErrorO 如果产 格式化或 出 则 回true<sup>0</sup> 一旦 个流 到了错误 它就受到了污 染 并且所有对checkError 将 回true<sup>o</sup>*

# *2.1.6如何 入文本 <sup>入</sup>*

*<sup>最</sup> <sup>单</sup> <sup>处</sup> 任意文本 方式就是使 在卷I中我们广泛使 Scanner 。我们可以 从任何 入流中构建Scanner对 。*

*或 我们也可以将 小 文本文件像下 样 人到一个字 串中*

*String content <sup>=</sup> Files.readstring(path, charset);*

*但是 如果想 将 个文件一行行地 人 么可以调用*

*List<String> lines <sup>=</sup> Files.readAULines(path, charset);*

*如果文件太大 么可以将 惰性处 为一个Stream<String>对*

```
try (Stream<String> lines = Files.lines(path, charset))
```

*可以使 扫描器来 入 号(token),即 分 分 字 串 分 是 字 。可以将分 修改为任意 正则 式。例如 下面的代*

```
Scanner in =..
in.useDelimiter("\\PL+ );
```

*将接受任何 Unicode字母作为分 。之后 个扫描器将只接受Unicode字母。*

*next方法可以产 下一个 号*

```
while (In.hasNextO)
```

```
String word = in.next();

}
或者,可以像下面这样获取一个包含所有符号的流:
Stream<String> words = in.tokens();
```

在早期的 Java 版本中,处理文本输入的唯一方式就是通过 BufferedReader 类。它的 read-Line 方法会产生一行文本,或者在无法获得更多的输入时返回 null。典型的输入循环看起来 像下面这样:

```
InputStream inputStream = . . .;
try (var in = new BufferedReader(new InputStreamReader(inputStream, charset)))
{
   boolean done = false;
   while (!done)
   {
      String line = in.readLine();
      if (line == null) done = true;
      else
      {
            do something with line
      }
   }
}
```

如今,BufferedReader 类又有了一个 lines 方法,可以产生一个 Stream<String> 对象。但是,与 Scanner 不同,BufferedReader 没有任何用于读入数字的方法。

# 2.1.7 以文本格式存储对象

在本节,我们将带你领略一个示例程序,它将一个 Employee 记录数组存储成了一个文本文件,其中每条记录都保存成单独的一行,而实例字段彼此之间使用分隔符分离开,这里我们使用竖线(|)作为分隔符(冒号(:)是另一种流行的选择,有趣的是,每个人都会使用不同的分隔符)。因此,我们这里假设在要存储的字符串中不存在 |。

下面是一个记录集的样本:

```
Harry Hacker|35500|1989-10-01
Carl Cracker|75000|1987-12-15
Tony Tester|38000|1990-03-15
```

写出记录相当简单,因为是要写出到一个文本文件中,所以我们使用 PrintWriter 类。我们直接写出所有的字段,每个字段后面跟着一个 |,而最后一个字段的后面跟着一个换行符。这项工作是在下面这个我们添加到 Employee 类中的 writeEmployee 方法里完成的:

```
public static void writeEmployee(PrintWriter out, Employee e)
{
   out.println(e.getName() + "|" + e.getSalary() + "|" + e.getHireDay());
}
```

为了读入记录,我们每次读入一行,然后分离所有的字段。我们使用一个扫描器来读入每一行,然后用 String.split 方法将这一行断开成一组符号。

```
public static Employee readEmployee(Scanner in)
{
   String line = in.nextLine();
   String[] tokens = line.split("\\|");
   String name = tokens[0];
   double salary = Double.parseDouble(tokens[1]);
   LocalDate hireDate = LocalDate.parse(tokens[2]);
   int year = hireDate.getYear();
   int month = hireDate.getMonthValue();
   int day = hireDate.getDayOfMonth();
   return new Employee(name, salary, year, month, day);
}
```

split 方法的参数是一个描述分隔符的正则表达式,我们在本章的末尾将详细讨论正则表达式。碰巧的是,竖线在正则表达式中具有特殊的含义,因此需要用\字符来表示转义,而这个\又需要用另一个\来转义,这样就产生了"\\\"表达式。

完整的程序如程序清单 2-1 所示。静态方法

```
void writeData(Employee[] e, PrintWriter out)
```

首先写出该数组的长度, 然后写出每条记录。静态方法

```
Employee[] readData(Scanner in)
```

首先读入该数组的长度,然后读入每条记录。这显得稍微有点棘手:

```
int n = in.nextInt();\nin.nextLine(); // consume newline
var employees = new Employee[n];
for (int i = 0; i < n; i++)
{
   employees[i] = new Employee();
   employees[i].readData(in);
}</pre>
```

对 nextInt 的调用读入的是数组长度,但不包括行尾的换行字符,我们必须处理掉这个换行符,这样,在调用 nextLine 方法后,readData 方法就可以获得下一行输入了。

#### 程序清单 2-1 textFile/TextFileTest.java

```
package textFile;\nimport java.io.*;\nimport java.nio.charset.*;\nimport java.time.*;\nimport java.util.*;

/**
    * @version 1.15 2018-03-17
    * @author Cay Horstmann
    */
public class TextFileTest
{
    public static void main(String[] args) throws IOException
{
}
```

```
var staff = new Employee[3];
16
17
         staff[0] = new Employee("Carl Cracker", 75000, 1987, 12, 15);
18
         staff[1] = new Employee("Harry Hacker", 50000, 1989, 10, 1);
19
         staff[2] = new Employee("Tony Tester", 40000, 1990, 3, 15);
20
21
         // save all employee records to the file employee.dat
22
         try (var out = new PrintWriter("employee.dat", StandardCharsets.UTF 8))
23
24
         {
             writeData(staff, out);
25
26
27
         // retrieve all records into a new array
28
         try (var in = new Scanner(
29
                new FileInputStream("employee.dat"), "UTF-8"))
38
31
             Employee[] newStaff = readData(in);
32
33
             // print the newly read employee records
34
             for (Employee e : newStaff)
35
                System.out.println(e);
36
37
      }
38
30
       /**
48
        * Writes all employees in an array to a print writer
41
        * @param employees an array of employees
42
        * @param out a print writer
43
44
       private static void writeData(Employee[] employees, PrintWriter out)
45
             throws IOException
46
47
          // write number of employees
4R
          out.println(employees.length);
49
50
          for (Employee e : employees)
51
             writeEmployee(out, e);
52
       }
53
54
55
        * Reads an array of employees from a scanner
56
        * @param in the scanner
57
        * @return the array of employees
58
59
       private static Employee[] readData(Scanner in)
68
61
          // retrieve the array size
62
          int n = in.nextInt():
63
          in.nextLine(); // consume newline
64
65
          var employees = new Employee[n];
66
          for (int i = 0; i < n; i++)
67
68
             employees[i] = readEmployee(in);
69
```

```
70
         return employees;
71
72
73
74
       * Writes employee data to a print writer
75
       * @param out the print writer
76
77
      public static void writeEmployee(PrintWriter out, Employee e)
78
79
         out.println(e.getName() + "|" + e.getSalary() + "|" + e.getHireDay());
88
81
82
      /**
83
       * Reads employee data from a buffered reader
84
       * @param in the scanner
25
86
      public static Employee readEmployee(Scanner in)
87
RR
         String line = in.nextLine();
89
         String[] tokens = line.split("\\|");
98
         String name = tokens[0];
91
         double salary = Double.parseDouble(tokens[1]);
92
         LocalDate hireDate = LocalDate.parse(tokens[2]);
93
         int year = hireDate.getYear();
94
         int month = hireDate.getMonthValue();
95
         int day = hireDate.getDayOfMonth();
96
         return new Employee(name, salary, year, month, day);
97
      }
98
99 }
```

### 2.1.8 字符编码方式

输入和输出流都是用于字节序列的,但是在许多情况下,我们希望操作的是文本,即字符序列。于是,字符如何编码成字节就成了问题。

Java 针对字符使用的是 Unicode 标准。每个字符或"编码点"都具有一个 21 位的整数。有多种不同的字符编码方式,也就是说,将这些 21 位数字包装成字节的方法有多种。

最常见的编码方式是UTF-8,它会将每个Unicode编码点编码为1到4个字节的序列(请参阅表2-1)。UTF-8的好处是传统的包含了英语中用到的所有字符的ASCII字符集中的每个字符都只会占用一个字节。

| 字符范围        | 编码方式                                                                                                                                                                                                                                                          |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 07F         | $\theta a_6 a_5 a_4 a_3 a_2 a_1 a_8$                                                                                                                                                                                                                          |
| 807FF       | 110a <sub>18</sub> a <sub>9</sub> a <sub>6</sub> a <sub>7</sub> a <sub>6</sub> 10a <sub>5</sub> a <sub>4</sub> a <sub>3</sub> a <sub>2</sub> a <sub>1</sub> a <sub>8</sub>                                                                                    |
| 800FFFF     | 1110a <sub>15</sub> a <sub>14</sub> a <sub>13</sub> a <sub>12</sub> 10a <sub>11</sub> a <sub>10</sub> a <sub>9</sub> a <sub>8</sub> a <sub>7</sub> a <sub>6</sub> 10a <sub>5</sub> a <sub>4</sub> a <sub>3</sub> a <sub>2</sub> a <sub>1</sub> a <sub>8</sub> |
| 1000010FFFF | 11110a26a26a18 10a17a16a25a14a13a12 10a11a16a8a87a6 10a5a4a3a2a1a6                                                                                                                                                                                            |

表 2-1 UTF-8 编码方式

另一种常见的编码方式是 UTF-16, 它会将每个 Unicode 编码点编码为 1 个或 2 个 16 位值 (请参阅表 2-2)。这是一种在 Java 字符串中使用的编码方式。实际上,有两种形式的 UTF-16,被称为 "高位优先"和 "低位优先"。考虑一下 16 位值 0x2122。在高位优先格式中,高位字节会先出现: 0x21 后面跟着 0x22。但是在低位优先格式中,是另外一种排列方式: 0x22 0x21。为了表示使用的是哪一种格式,文件可以以 "字节顺序标记" 开头,这个标记为 16 位数值 0xFEFF。读入器可以使用这个值来确定字节顺序,然后丢弃它。

| 72 2-2 011 -10 Sid H-3/12C |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |  |
|----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|
| 字符范围                       | 编码方式                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |  |
| 0FFFF                      | a15a14a13a12a11a18a8a a7a6a3a4a3a2a1a8                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |  |
| 1000010FFFF                | 110110b <sub>19</sub> b <sub>18</sub> b <sub>17</sub> b <sub>16</sub> a <sub>15</sub> a <sub>14</sub> a <sub>15</sub> a <sub>12</sub> a <sub>12</sub> a <sub>12</sub> a <sub>13</sub> 110111a <sub>9</sub> a <sub>8</sub> a <sub>7</sub> a <sub>6</sub> a <sub>5</sub> a <sub>4</sub> a <sub>3</sub> a <sub>2</sub> a <sub>1</sub> a <sub>8</sub><br>其中 b <sub>19</sub> b <sub>18</sub> b <sub>17</sub> b <sub>16</sub> = a <sub>28</sub> a <sub>18</sub> a <sub>18</sub> a <sub>17</sub> a <sub>16</sub> - 1 |  |

表 2-2 UTF-16 编码方式

● 警告:有些程序,包括 Microsoft Notepad (微软记事本)在内,都在 UTF-8 编码的文件开头处添加了一个字节顺序标记。很明显,这并不需要,因为在 UTF-8 中,并不存在字节顺序的问题。但是 Unicode 标准允许这样做,甚至认为这是一种好的做法,因为这样做可以使编码机制不留疑惑。遗憾的是,Java 并没有这么做,有关这个问题的缺陷报告最终是以"will not fix"(不做修正)关闭的。对你来说,最好的做法是将输入中发现的所有先导的 \uFEFF 都剥离掉。

除了 UTF 编码方式,还有一些编码方式,它们各自都覆盖了适用于特定用户人群的字符范围。例如,ISO 8859-1 是一种单字节编码,它包含了西欧各种语言中用到的带有重音符号的字符,而 Shift-JIS 是一种用于日文字符的可变长编码。类似这些的大量编码方式至今仍被广泛使用。

不存在任何可靠的方式可以自动地探测出字节流中所使用的字符编码方式。某些 API 方法让我们使用"默认字符集",即计算机的操作系统首选的字符编码方式。这种字符编码方式与我们的字节源中所使用的编码方式相同吗?字节源中的字节可能来自世界上的其他国家或地区,因此,你应该总是明确指定编码方式。例如,在编写网页时,应该检查 Content-Type 头信息。

- 註释: 平台使用的编码方式可以由静态方法 Charset.defaultCharset 以及系统属性 native.encoding 返回。如果使用的是用于用户交互的 Console 类,那么调用其 charset 方法就可以获取控制台的字符集。静态方法 Charset.availableCharsets 会返回所有可用的 Charset 实例,返回结果是一个从字符集的规范名称到 Charset 对象的映射表。
- 警告: Oracle 的 Java 实现有一个用于覆盖平台默认值的系统属性 file.encoding。但是它并非官方支持的属性,并且 Java 库的 Oracle 实现的所有部分并非都以一致的方式处理该属性,因此,你不应该设置它。

StandardCharsets 类具有类型为 Charset 的静态变量,用于表示每种 Java 虚拟机都必须支持的字符编码方式:

StandardCharsets.UTF\_8 StandardCharsets.UTF\_16 StandardCharsets.UTF\_16BE StandardCharsets.UTF\_16LE StandardCharsets.ISO\_8859\_1 StandardCharsets.US\_ASCII

为了获得另一种编码方式的 Charset, 可以使用静态的 forName 方法:

Charset shiftJIS = Charset.forName("Shift-JIS");

在读入或写出文本时,应该使用 Charset 对象。例如,我们可以像下面这样将一个字节数组转换为字符串:

var str = new String(bytes, StandardCharsets.UTF\_8);

- ☑ 提示:在 Java 10 中, java.io 包中的所有方法都允许我们用一个 Charset 对象或字符串来指定字符编码方式。应该选择的是 StandardCharsets 常量,这样就可以在编译时捕获到所有拼写错误了。
- 警告: 在不指定任何编码方式时,有些方法 (例如 String(byte[]) 构造器) 会使用默认的平台编码方式,而其他方法 (例如 Files.readAllLines) 会使用 UTF-8。
- i 注释: 自 Java 17 以后, UTF-8 将成为 JDK 的默认值, 不管平台的编码方式到底是什么。至此之前, 你要确保将所有的编码方式都指定为 StandardCharsets.UTF\_8, 除非你知道自己需要的与其不同的编码方式, 然后明确指定你想要的编码方式。

# 2.2 读写二进制数据

文本格式对于测试和调试而言会显得很方便,因为它是人类可阅读的,但是它并不像以二进制格式传递数据那样高效。在下面的各小节中,你将会学习如何用二进制数据来完成输入和输出。

# 2.2.1 DataInput 和 DataOutput 接口

DataOutput 接口定义了下面用于以二进制格式写数组、字符、boolean 值和字符串的方法:

writeChars writeFloat
writeByte writeDouble
writeInt writeChar
writeShort writeBoolean
writeLong writeUTF

例如, writeInt 总是将一个整数写出为 4 字节的二进制数量值,而不管它有多少位, write-Double 总是将一个 double 值写出为 8 字节的二进制数量值。这样产生的结果并非人可阅读的,但是对于给定类型的每个值,使用的空间都是相同的,而且将其读回也比解析文本要更快。

**注释**:根据你所使用的处理器类型,在内存存储整数和浮点数有两种不同的方法。例

*<sup>如</sup> <sup>假</sup> 你使 <sup>是</sup>4<sup>字</sup> int,如果有一个十 制數1234,也就是十六 <sup>制</sup> 4D2 ( <sup>1234</sup> <sup>=</sup> 4x256十13x16 <sup>+</sup> 2), 么它可以按照内存中4<sup>字</sup> 一个字 <sup>存</sup> 储最 位字 方式来存储为<sup>00</sup> <sup>0</sup> 04D2, 就是所 位在前 序(MSB);<sup>我</sup> 们也可以从最低位字 开始 即D2 <sup>04</sup> <sup>00</sup> 90, 方式 然就是所 低位在前 序 (LSB)0例如 SPARC<sup>使</sup> <sup>是</sup> 位在前 <sup>序</sup> Pentium<sup>使</sup> 则是低位在前 <sup>序</sup>。 就可 会带来 当存储C或 C++文件时 數据会 地按照处 器存储它 们 方式来存储 就使得即使是最 单 數据在从一个平台 到另一个平台上时 也是一 挑战。在Java中 所有 值 按照 位在前 模式写出 不 使 何 处 器 使得Java数据文件可以 于平台。*

*writeUTF方法使 修 8位Unicode 换格式写出字 串。 方式与 接使 标准 UTF-8 方式不同 其中 Unicode 元序列先 UTF-16 然后其 果使 UTF-8 则 。修 后 方式对于 大于OxFFFF 字 处 有所不同 是 为了向后兼容在Unicode 没有超过16位时构建 拟机。*

*因为没有其他方法会使 UTF-8的这种修 所以你应 只在写出 于Java 拟机 字 串时才使 writeUTF方法 例如 当你 写一个 成字 序时。对于其他场 合 应 使 writeChars方法。*

*为了 回数据 可以使 在Datal<sup>叩</sup>ut接口中定义 下列方法*

*readlnt readDouble*

*readShort readChar*

*readLong readBoolean*

*readFloat readUTF*

*DatalnputStream 实 了 Datalnput接口 为了从文件中 入二 制数据 可以将Datalnput-Stream与某个字 源 合 例如FilelnputStream*

*var in <sup>=</sup> new DatalnputStream(new FilelnputStream("employee.dat"));*

*与此 似 想写出二 制数据 你可以使 实 了 DataOutput接口 DataOutputStream var out <sup>=</sup> new DataOutputStream(new FileOutputSt ream("employee.dat ));*

# *am] java.io.Datalnput*

- *• boolean readBoolean()*
- *• byte readByteO*
- *• char readChar()*
- *• double readDouble()*
- *<sup>參</sup> float readFloat()*
- *• int readlnt()*
- *• long readLong()*
- *• short readShort() 入一个 定 型 值。*

- void readFully(byte[] b)将字节读入到数组 b 中, 其间阻塞直至所有字节都读入。
- void readFully(byte[] b, int off, int len) 将由 len 指定数量的字节放置到数组 b 从 off 开始的位置,其间阻塞直至所有字节都读人。
- String readUTF() 读入由"修订过的 UTF-8"格式的字符构成的字符串。
- int skipBytes(int n)跳过 n 个字节,其间阻塞直至所有字节都被跳过。

#### API java.io.DataOutput

- void writeBoolean(boolean b)
- void writeByte(int b)
- void writeChar(int c)
- void writeDouble(double d)
- void writeFloat(float f)
- void writeInt(int i)
- void writeLong(long l)
- void writeShort(int s)写出一个给定类型的值。
- void writeChars(String s)
   写出字符串中的所有字符。
- void writeUTF(String s)
   写出由"修订过的 UTF-8"格式的字符构成的字符串。

#### 2.2.2 随机访问文件

RandomAccessFile 类可以在文件中的任何位置读取或写入数据。磁盘文件都是随机访问的,但是与网络套接字通信的输入/输出流却不是。你可以打开一个随机访问文件,只用于读入或者同时用于读写,你可以通过使用字符串"r"(用于读入访问)或"rw"(用于读入/写出访问)作为构造器的第二个参数来指定这个选项。

var in = new RandomAccessFile("employee.dat", "r");
var inOut = new RandomAccessFile("employee.dat", "rw");

当你将已有文件作为 RandomAccessFile 打开时,这个文件并不会被删除。

随机访问文件有一个表示下一个将被读入或写出的字节所处位置的文件指针, seek 方法可以用来将这个文件指针设置到文件中的任意字节位置, seek 的参数是一个 long 类型的整数, 它的值位于 0 到文件按照字节来度量的长度之间。

getFilePointer 方法将返回文件指针的当前位置。

RandomAccessFile 类同时实现了 DataInput 和 DataOutput 接口。为了读写随机访问文件,可以使用在前面小节中讨论过的诸如 readInt/writeInt 和 readChar/writeChar 之类的方法。

我们现在要剖析一个将雇员记录存储到随机访问文件中的示例程序,其中每条记录都拥有相同的大小,这样我们可以很容易地读入任何记录。假设你希望将文件指针置于第三条记录处,那么你只需将文件指针置于恰当的字节位置,然后就可以开始读入了。

```
long n = 3;
in.seek((n - 1) * RECORD_SIZE);
var e = new Employee();
e.readData(in);
```

如果你希望修改记录,然后将其存回到相同的位置,那么请切记要将文件指针置回到这条记录的开始处:

```
in.seek((n - 1) * RECORD_SIZE);\ne.writeData(out);
```

要确定文件中的字节总数,可以使用 length 方法,而记录的总数则等于用字节总数除以每条记录的大小。

```
long nbytes = in.length(); // length in bytes\nint nrecords = (int) (nbytes / RECORD_SIZE);
```

整数和浮点值在二进制格式中都具有固定的尺寸,但是在处理字符串时就有些麻烦了,因此我们提供了两个助手方法来读写具有固定尺寸的字符串。

writeFixedString 写出从字符串开头开始的指定数量的码元(如果码元过少,该方法将用 0 值来补齐字符串)。

```
public static void writeFixedString(String s, int size, DataOutput out)
```

readFixedString 方法从输入流中读入字符,直至读入 size 个码元,或者直至遇到 具有 0 值的字符值,然后跳过输入字段中剩余的 0 值。为了提高效率,这个方法使用了 StringBuilder 类来读入字符串。

```
public static String readFixedString(int size, DataInput in)
```

```
i++;\nif (ch == 0) done = true;\nelse b.append(ch);
}\nin.skipBytes(2 * (size - i));
return b.toString();
}
```

我们将 writeFixedString 和 readFixedString 方法放到了 DataIO 助手类的内部。 为了写出一条固定尺寸的记录,我们直接以二进制方式写出所有的字段:

```
DataIO.writeFixedString(e.getName(), Employee.NAME_SIZE, out);
out.writeDouble(e.getSalary());
LocalDate hireDay = e.getHireDay();
out.writeInt(hireDay.getYear());
out.writeInt(hireDay.getMonthValue());
out.writeInt(hireDay.getDayOfMonth());
```

#### 读回数据也很简单:

```
String name = DataIO.readFixedString(Employee.NAME_SIZE, in);
double salary = in.readDouble();\nint y = in.readInt();\nint m = in.readInt();\nint d = in.readInt();
```

让我们来计算每条记录的大小: 我们将使用 40 个字符来表示姓名字符串, 因此, 每条记录包含 100 个字节:

- 40 字符 = 80 字节, 用于姓名。
- 1 double = 8 字节, 用于薪水。
- 3 int = 12 字节, 用于日期。

程序清单 2-2 中所示的程序将三条记录写到了一个数据文件中,然后以逆序将它们从文件中读回。为了高效地执行,这里需要使用随机访问,因为我们需要首先读入第三条记录。

# 程序清单 2-2 randomAccess/RandomAccessTest.java

```
package randomAccess;
2
3 import java.io.*;
4 import java.time.*;
5
6 /**
   * @version 1.14 2018-05-01
    * @author Cay Horstmann
9
  public class RandomAccessTest
18
11
  {
      public static void main(String[] args) throws IOException
12
13
         var staff = new Employee[3];
14
15
         staff[0] = new Employee("Carl Cracker", 75000, 1987, 12, 15);
16
         staff[1] = new Employee("Harry Hacker", 50000, 1989, 10, 1);
17
```

```
staff[2] = new Employee("Tony Tester", 40000, 1990, 3, 15);
18
19
         try (var out = new DataOutputStream(new FileOutputStream("employee.dat")))
20
21
            // save all employee records to the file employee.dat
22
             for (Employee e : staff)
23
                writeData(out, e):
24
25
26
         try (var in = new RandomAccessFile("employee.dat", "r"))
27
28
             // retrieve all records into a new array
29
30
             // compute the array size
31
             int n = (int)(in.length() / Employee.RECORD SIZE);
32
             var newStaff = new Employee[n];
33
34
             // read employees in reverse order
35
             for (int i = n - 1; i >= 0; i - -)
36
             {
37
                newStaff[i] = new Employee();
38
                in.seek(i * Employee.RECORD SIZE);
39
                newStaff[i] = readData(in);
48
41
             }
42
             // print the newly read employee records
43
             for (Employee e : newStaff)
44
                System.out.println(e);
45
46
47
48
49
        * Writes employee data to a data output
50
        * @param out the data output
51
        * @param e the employee
52
        */
53
       public static void writeData(DataOutput out, Employee e) throws IOException
54
55
          DataIO.writeFixedString(e.getName(), Employee.NAME SIZE, out);
56
          out.writeDouble(e.getSalary());
57
58
          LocalDate hireDay = e.getHireDay();
59
          out.writeInt(hireDay.getYear());
60
          out.writeInt(hireDay.getMonthValue());
61
          out.writeInt(hireDay.getDayOfMonth());
62
       }
63
64
65
        * Reads employee data from a data input
66
        * @param in the data input
67
        * @return the employee
6R
69
       public static Employee readData(DataInput in) throws IOException
78
71
          String name = DataIO.readFixedString(Employee.NAME SIZE, in);
72
```

```
double salary = in.readDouble();\nint y = in.readInt();\nint m = in.readInt();\nint d = in.readInt();
return new Employee(name, salary, y, m - 1, d);
}

}
```

#### API java.io.RandomAccessFile 10

- RandomAccessFile(String file, String mode)
- RandomAccessFile(File file, String mode)
   打开给定的用于随机访问的文件。mode 字符串 "r"表示只读模式; "rw"表示读/写模式; "rws"表示每次更新时,都对数据和元数据的写磁盘操作进行同步的读/写模式: "rwd"表示每次更新时,只对数据的写磁盘操作进行同步的读/写模式。
- long getFilePointer()
   返回文件指针的当前位置。
- void seek(long pos)将文件指针设置到距文件开头 pos 个字节处。
- long length()返回文件按照字节来度量的长度。

#### 2.2.3 ZIP 文档

ZIP 文档(通常)以压缩格式存储了一个或多个文件,每个 ZIP 文档都有一个头,包含诸如每个文件的名字和所使用的压缩方法等信息。在 Java 中,可以使用 ZipInputStream 来读人 ZIP 文档。你可能需要浏览文档中每个单独的项,getNextEntry 方法就可以返回一个描述这些项的 ZipEntry 类型的对象。该方法会从流中读入数据直至末尾,实际上这里的末尾是指正在读入的项的末尾,然后调用 closeEntry 来读入下一项。直至读入最后一项之前,都不要关闭 zin。下面是典型的通读 ZIP 文件的代码序列:

```
var zin = new ZipInputStream(new FileInputStream(zipname));
boolean done = false;
while (!done)
{
    ZipEntry entry = zin.getNextEntry();
    if (entry == null) done = true;
    else
    {
        read the contents of zin
        zin.closeEntry();
    }
}
zin.close();
```

要写出到 ZIP 文件,可以使用 ZipOutputStream,而对于你希望放入到 ZIP 文件中的每一项,都应该创建一个 ZipEntry 对象,并将文件名传递给 ZipEntry 的构造器,它将设置其他诸如

*文件日期和 压 方法 参数。如果 你可以 些 。然后 你需要调用ZipOutputStream putNextEntry方法来写出新文件 并将文件数据发 到ZIP 出流中。当完成时 closeEntry0然后 <sup>你</sup> 对所有希望存储 文件 <sup>复</sup> <sup>个</sup> 。<sup>下</sup> 是代 框架*

```
var tout = new FileOutputStream("test.zip");
var zout « new ZipOutputStreal(tout):
for allfiles
{
   var ze = new lipEntry(filename);
   zout.putNextEntry(ze);
   send data to zout
   zout.closeEntryO;
}
zout. closed;
```

*Q <sup>注</sup> JAR文件(在卷I <sup>4</sup> <sup>中</sup> )只是带有一个 <sup>殊</sup> ZIP文件 <sup>个</sup> 作清单。你可以使 JarlnputStream和JarOutputStream 来 写清单 。*

*ZIP 人流是一个 够展 流 抽 化 强大之处 实例。当你 入以压 格式存储 数据时 不必担心 求 压数据 且ZIP格式 字 源并 必 是文件 也可 以是来 接 ZIP数据。*

*0 <sup>注</sup> 2.4.8 将展 如何使 Java <sup>7</sup> FileSystem <sup>无</sup> <sup>殊</sup>API<sup>来</sup> ZIP文档。*

# *java.util.zip.ZipInputStream*

- *• Zipl叩utStream(I叩utStream in) 创建一个Zipl叩utStream,使得我们可以从 定 Inputstream向其中填充数据。*
- *• ZipEntry getNextEntryO 为下一 回ZipEntry对 或 在没有更多 时 回null*
- *• void closeEntryO 关 个ZIP文件中当前打开 。之后可以 使 getNextEntryO 入下一 。*

# *Ani java.util.zip.ZipOutputStrean*

- *• ZipOutputStream(OutputStream out) 创建一个将压 数据写出到指定 OutputStream ZipOutputStream<sup>o</sup>*
- *• void putNextEntry(ZipEntry ze) 将 定 ZipEntry中 信息写出到 出流中 并定位 于写出数据 流 然后 些数 据可以通过write()写出到 个 出流中。*
- *• void closeEntryO 关 个ZIP文件中当前打开 。使 putNextEntry方法可以开始下一 。*
- *• void setLevel(int level) 将后 各个DEFLATED 压 别 为从Deflater. NO COMPRESSION<sup>到</sup>*

*Deflater.BEST\_COMPRESSION 中 某个值 值是 DeHater.DEFAULT\_COMPRESSION 如果 别无效 则抛出 IllegalArgumentException*

*• void setMethod(int method) 于 个ZipOutputStream 压 方法 个压 方法会作 于所有没有指定 压 方法 。method可以是DEFLATED或STORED*

# *java. util. zip. ZipEntry*

- *• ZipEntry(String name) 定 名字构建一个ZIP 。*
- *• long getCrc() 回 于 个ZipEntry CRC32校 和 值。*
- *• String getNameO 回 一 名字。*
- *• long getSizeO 回 一 未压 尺寸 或 在未压 尺寸不可 情况下 回-1。*
- *• boolean isDirectoryO 当 一 是 录时 回true*
- *• void setMethod(int method) 于 一 压 方法 必 是DEFLATED或STORED*
- *• void setSize(long size) 一 尺寸 只有在压 方法是STORED时才是必 。*
- *• void setCrc(long crc) 给这一项设置CRC32校 和 个校 和是使 CRC32 。只有在压 方法 是STORED时才是必 。*

# *^jjava.util.zip.ZipFile*

- *• ZipFile(String name)*
- *• ZipFile(File file) 创建一个ZipFile, 于从 定 字 串或File对 中 入数据。*
- *• Enumeration entries!) 回一个Enumeration对 它枚举了描 个ZipFile中各个项的ZipEntry对 。*
- *• ZipEntry getEntry(Strlng name) 回 定名字所对应 或 在没有对应 时候 回null*
- *• InputStream getInputSt ream(ZipEnt ry ze) 回 于 定 InputStreamo*
- *• String getNameO 回 个ZIP文件的路径。*

# *2.3<sup>对</sup> <sup>入</sup>/ 出流与序列化*

*当你 存储 同 型 数据时 使 固定 度 录格式是一个不 择。但是 在 向对 序中创建 对 很少全 具有 同 型。例如 你可 有一个 为staff 数 它名义上是一个Employee 录数 但是实 上却包含 如Manager 样 子 实例。*

*我们当然可以 己 出一 数据格式来存储 多态 合 但是幸 是 我们并不需要 么做。Java 支持一 为对 序列化(ottject serialization) 常 机制 它可以将任 何对 写出到 出流中 并在之后将其 回。(你将在木 后 到"序列化" 个术 出处。)*

# *2.3.1保存和加 序列化对*

*为了保存对 数据 先 打开一个Objectoutputstream对*

*var out <sup>=</sup> new Obj ectOutputStream(new FileOutputStream("employee.dat\*));*

*在 为了保存对 可以 接使 Obj ectOutputStream writeObject方法 如下所*

```
var harry = new Employee{'Harry Hacker", 50060, 1989, 10, 1);
var boss = new Manager("Carl Cracker", 80❷❷0, 1987, 12r 15);
out.writeObject(harry);
out.writeObject(boss);
```

*为了将 些对 回 先 得一个ObjectlnputStream对*

*var in <sup>=</sup> new ObjectI叩utStream(new Filel叩utStreau(\_employee.dat B;*

*然后 readobject方法以 些对 写出时 序 取它们*

```
var el = (Employee) in.readObjectO;
var e2 = (Employee) in.readObjectO;
```

*但是 对希望在对 出流中存储或从对 人流中恢复 所有 应 一下修改 些 必 实 Serializable接口*

```
class Employee inplenents Serializable { . . . }
```

*Serializable接口没有任何方法 因此你不 对 些 做任何改动。在 一点上 它 与在卷I <sup>6</sup> <sup>中</sup> Cloneable接口很 <sup>似</sup>。但是 为了使 可克 你仍旧需要覆 Object 中 clone方法 为了使 可序列化 你不 做任何事。*

*0 <sup>注</sup> 你只有在写出对 时才能用writeObj ect/readObject方法 对于基本 型值 <sup>你</sup> 使 如writelnt/readlnt或writeDouble/readDouble 样 方法。(对 入/ 出流 实 了 Datal叩ut/DataOutput接口。)*

*在幕后 是Obj ectOutputStream在浏 对 所有域 并存储它们 内容。例如 当写 出一个Employee对 时 其名字、日期和 水域 会 写出到 出流中。*

*但是 有一 情况 当一个对 多个对 共享 作为它们各 态 一 分时 会发 什么呢*

为了说明这个问题,我们对 Manager 类稍微做些修改, 假设每个经理都有一个秘书:

```
class Manager extends Employee
{
   private Employee secretary;
   . . .
}
```

现在每个 Manager 对象都包含一个表示秘书的 Employee 对象的引用,当然,两个经理可以共用一个秘书,正如图 2-5 和下面的代码所示的那样:

```
var harry = new Employee("Harry Hacker", . . .);
var carl = new Manager("Carl Cracker", . . .);
carl.setSecretary(harry);
var tony = new Manager("Tony Tester", . . .);
tony.setSecretary(harry);
```

![](_page_84_Figure_6.jpeg)

图 2-5 两个经理可以共用一个共有的雇员

保存这样的对象网络是一种挑战,在这里我们当然不能去保存和恢复秘书对象的内存地址,因为当对象被重新加载时,它可能占据的是与原来完全不同的内存地址。

每个对象都是用一个序列号(serial number)保存的,这就是这种机制之所以称为对象序列化的原因。下面是其算法:

- 对你遇到的每一个对象引用都关联一个序列号(如图 2-6 所示)。
- 对于每个对象, 当第一次遇到时, 保存其对象数据到输出流中。
- 如果某个对象之前已经被保存过,那么只写出"与之前保存过的序列号为 x 的对象相同"。 在读回对象时,整个过程是反过来的。
- 对于对象输入流中的对象,在第一次遇到其序列号时,构建它,并使用流中数据来初始化它,然后记录这个顺序号和新对象引用之间的关联。

*<sup>当</sup> <sup>到</sup>"与之前保存 序列号为\* 对象相同" 一标 <sup>时</sup> 取与 个序列号 关 对 引 。*

![](_page_85_Figure_3.jpeg)

*图2-6 —个对 序列化 实例*

- *注 在本 中 我们使 序列化将对 合保存到 文件中 并按照它们 存储 样子 取它们。序列化 另一 常 应 是 将对 合传 到另一 台计算机上。正如在文件中保存原 内存地址毫无意义一样 些地址对于在不同 处 器之 信也是毫无意义 。因为序列化 序列号代替了内存地址 所以它 允 将对 合从一台机器传 到另一台机器。*
- *0 <sup>告</sup> 正如在下一 中将 <sup>到</sup> <sup>对</sup> 流中包含了所有 序列化对 、 和域 名字。对于内部类 有些名字由编译器合成 其命名 可 会因 器不同 产 变化。如果 实发 了 变化 么反序列化就会失 。因此 你需要对内 序列化提 惕。 态内部类 包括内 枚举和 录 对于序列化来 是安 全 。*

*序清单2-3是保存和 新加 Employee和Manager对象网络的代 有些对 共享 同 书 员 。注意 书对 在 新加 之后是唯一 当newStaff[l] 恢复时 它会反映到 们 secretary域中。*

# *序清单 2-3 serial/ObjectStreamTest.java*

```
1 package serial;
2
3 import java.io.寧;
6
ie
n
12
13
14
15
16
17
18
19
2e
21
22
23
24
25
26
21
28
29
36
31
32
33
34
35
36
37
39
4
41
42
43
44
45
   /*
    * ^version 1.12 2021-09-1
      ^author Cay Horstmann
    V
   class ObjectStreanTest
   {
      public static void main(String!] args) throws IOException, ClassNotFoundException
      {
         var harry = new Employee("Harry Hacker", 50000, 1989, 10, 1);
         var carl = new Manager("Carl Cracker", 80 00, 1987, 12, 15);
          carl.setSecretary(harry);
         var tony = new Manager("Tony Tester", 40 00, 1999, 3, 15);
         tony.setSecretary(harry);
          var staff = new Employee[3];
          staff[0] = carl;
          staff[l] = harry;
          staff[2] = tony;
          // save all employee records to the file employee.ser
          try (var out = new ObjectOutputStream(new FileOutputStream(Memployee.serM)))
          {
             out.writeObject(staff);
          }
          try (var in = new ObjectInputStream(new FilelnputStream("employee.ser")))
             // retrieve all records into a new array
             var newStaff = (Employee!]) in.readObjectf);
             // raise secretary's salary
             newStaff[l].raiseSalary(lG);
             // print the newly read employee records
             for (Employee e : newStaff)
                System.out.println(e);
          }
       }
   }
```

# *ar<sup>|</sup> java.io.Obj ectOutputStream*

- *• Obj ectOutputStream(OutputStream out) 创建一个ObjectOutputStream使得你可以将对 写出到指定 Outputstream*
- *• void writeObject(Object obj)*

写出指定的对象到 ObjectOutputStream,这个方法将存储指定对象的类、类的签名以及这个类及其超类中所有非静态和非瞬时的域的值。

## API java.io.ObjectInputStream

- ObjectInputStream(InputStream in)
   创建一个 ObjectInputStream 用于从指定的 InputStream 中读回对象信息。
- Object readObject()

从 ObjectInputStream 中读入一个对象。特别是,这个方法会读回对象的类、类的签名以及这个类及其超类中所有非静态和非瞬时的域的值。它执行的反序列化允许恢复多个对象引用。

#### 2.3.2 理解对象序列化的文件格式

对象序列化是以特殊的文件格式存储对象数据的,当然,我们使用 writeObject/read-Object 方法时,并非必须要了解文件中表示对象的确切字节序列到底是怎样的。但是,我们发现研究这种数据格式对于洞察对象流化的处理过程非常有益。因为其细节显得有些专业,所以如果你对其实现不感兴趣,则可以跳过这一节。

每个文件都是以下面这两个字节的"魔幻数字"开始的

AC ED

后面紧跟着对象序列化格式的版本号,目前是

00 05

(我们在本节中统一使用十六进制数字来表示字节。)然后是它包含的对象序列,其顺序即它们存储的顺序。

字符串对象被存为

- 72
- 2字节表示的字符串长度
- 以"修订的 UTF-8"格式表示的字符

例如,字符串"Harry"被存为

74 00 05 Harry

当存储一个对象时,这个对象所属的类也必须存储。这个类的描述符具有下面的格式:

- 72
- 2字节的类名长度
- 类名
- 8字节长的指纹
- 1字节长的标志
- 2字节长的实例域描述符的数量
- 实例域描述符
- 78 (结束标记)
- 超类类型(如果没有就是70)

*指 是 对 、 、接口、域 型和方法 名按照 方式排序 然后将安全散列 法<sup>1</sup> SHA-1 应 于 些数据 得 。*

*SHA-1是一 可以为信息块提供指 快 法 不 最初 数据块尺寸有多大 这种 指 总是20个字 数据包。它是 在数据上执 一个灵巧 位操作序列 创建 个序列在本 上可以 分之 地保 无 些数据以何 方式发 变化 其指 也 会 变化。但是 序列化机制只使 了 SHA-1 前8个字 作为 指 。即便 样 当类的 数据域或方法发 变化时 其指 变化 可 性 是 常大。*

*在 人一个对 时 会拿其指 与它所属 当前指 比对 如果它们不匹 , 么就 明 个类的定义在 对象被写出之后发生过变化 因此会产 一个异常。在实 情 况下 当然是会演化 因此对于 序来 人 旧 本 对 可 是必 。我们将 在2.3.5 中 个 。*

*标志字 是 在]ava. io. Obj ectStreamconstants中定义 位掩 构成 如 2-3所 。*

| 名                 | 值  | 描                                         |
|-------------------|----|-------------------------------------------|
| SC WRITE METHOD   | 1  | 定义writeObject的类                           |
| SC SERIALIZABLE   | 2  | 实<br>Serializable                         |
| SC EXTERNALIZABLE | 4  | 实<br>Extemalizable                        |
| SCJLOCK DATA      | 8  | 以<br>"块数据"写出<br>不<br>明数据<br>JDK1.2以来<br>值 |
| SC ENIW           | 16 | 枚举                                        |

*2-3位掩*

*我们 写出 些 实 了 Serializable接口 并且其标志值为02, 可序列化 java. util.Date 定义了它 己 readObject/writeObject方法 并且其标志值为03。*

*每个数据域描 格式如下*

- *• 1字节长的类型编码*
- *・2字 域名 度*
- *域名*
- *名 如果域是对*

*其中 型 是下列取值之一*

*<sup>B</sup> byte <sup>C</sup> char <sup>D</sup> double <sup>F</sup> float I int J long <sup>L</sup> 又橡 <sup>S</sup> short Z boolean [ 数*

76

当类型编码为 L 时,域名后面紧跟域的类型。类名和域名字符串不是以字符串编码 74 开头的,但域类型是。域类型使用的是与域名稍有不同的编码机制,即本地方法使用的格式。

例如, Employee 类的薪水域被编码为:

D 00 06 salary

下面是 Employee 类完整的类描述符,包含在我们给出的示例程序的 serial 包中:

72 00 OF serial. Employee

74 1E C8 E6 C3 F8 B8 77 02

指纹和标志

00 03

实例域的数量

D 00 06 salary

实例域的类型和名字

L 00 07 hireDay

实例域的类型和名字

74 00 10 Ljava/util/Date;

实例域的类名: Date

L 00 04 name

实例域的类型和名字

74 00 12 Ljava/lang/String;

实例域的类名: String

78

结束标记

70

无超类

这些描述符相当长,如果在文件中再次需要相同的类描述符,可以使用一种缩写版:

71 4字节长的序列号

这个序列号将引用前面已经描述过的类描述符,我们稍后将讨论编号模式。对象将被存储为:

73 类描述符 对象数据

例如,下面展示的就是 Employee 对象如何存储:

40 E8 6A 00 00 00 00 00

salary域的值: double

73

hireDate 域的值:新对象

71 00 7E 00 08

已有的类 java.util.Date

77 08 00 00 00 91 19 97 3D 80 78

外部存储, 稍后讨论细节

74 00 0C Harry Hacker

name域的值: String

正如你所看见的,数据文件包含了足够的信息来恢复这个 Employee 对象(在这个示例中,我们将雇佣日存储为 Date 而不是 LocalDate,因为 LocalDate 类的序列化更加复杂。)。

数组总是被存储成下面的格式:

75 类描述符 4字节长的数组项的数量 数组项

在类描述符中的数组类名的格式与本地方法中使用的格式相同(它与在其他的类描述符中的类名稍微有些差异)。在这种格式中,类名以L开头,以分号结束。

例如, 3个 Employee 对象构成的数组写出时就像下面这样:

75

数组

72 00 0B [LEmployee;

新类,字符串长度,类名Employee[]

*40 05 D6 7E 3B BB F2 50 62 00 78 70 ee ee ee 3 指 嘛志 实侈烟 数 数组项的数*

*注意 Employee对 数 指 与Employee 指 并不 同。*

*所有对 包含数 和字 串 和所有 描 在存储到 出文件时 予了一个 序列号 个数字以<sup>00</sup> 7E <sup>00</sup> 00开头。*

*我们已经看到 任何 定类的完整 描述符只保存一次 后 描 将引 它。例 如 在前 例中 对Date 复引 就 为*

*71 7E ee 68*

*同 机制 于对 。如果 写出一个对之前存储 对 引 么 个引 也会以完全 同 方式存储 即71后 序列号 从上下文中可以很清楚地了 个 殊 序列引 是 描 是对 。*

*有些 例如Date 会以不 明数据块 方式存储对 态 它们会 为*

- *• 77 数据块 或7A 数据块*
- *• 1字 或4字节长的块 度*
- *块内容*
- *• <sup>78</sup>*

*最后 引 存储为*

*69 01*

*下 是前 小 中ObjectRefTest 序 带注 出。如果你喜欢 可以 个 序 然后査 其数据文件employee.dat 十六 制 并将其与注 列 比 。在 出中接 束 分 几 展 了对之前存储 对 引 。*

| AC ED ee 95                    | 文件头                                        |
|--------------------------------|--------------------------------------------|
| 75                             | 序列#1<br>数<br>staff                         |
| 12 [Lserial.Employee;<br>72    | 名Employee[]<br>新<br>、字<br>串<br>度、<br>序歹0#0 |
|                                |                                            |
| 40<br>5 D6 7E 3B BB F2 58<br>2 | 指<br>和标志                                   |
|                                | 实例域<br>数                                   |
| 78                             | 束标                                         |
| 7                              | 无                                          |
| ee ee ee<br>3                  | 数<br>数                                     |
| 73                             | :<br>staffie]<br>新对<br>序列                  |
| E serial.Manager<br>72 90      | 名<br>序列#2<br>新<br>、字<br>串<br>度、            |
| 2F FF IF ID E8 7A A9 74 62     | 指<br>和标志                                   |
|                                |                                            |

*实例域 数*

73

L 00 09 secretary 实例域的类型和名字 74 00 11 Lserial/Employee; 实例域的类名: String(序列#3) 结束标记 超类:新类、字符串长度、类名(序列#4) 72 00 OF serial. Employee 74 1E C8 E6 C3 F8 B8 77 02 指纹和标志 00 03 实例域的数量 D 00 06 salary 实例域的类型和名字 L 00 07 hireDay 实例域的类型和名字 74 00 10 Ljava/util/Date; 实例域的类名: String(序列#5) L 00 04 name 实例域的类型和名字 74 00 12 Ljava/lang/String; 实例域的类名: String(序列#6) 78 结束标记 70 无超类 salary 域的值: double 40 F3 88 00 00 00 00 00 hireDate 域的值:新对象(序列#9) 73 新类、字符串长度、类名(序列#8) 72 00 OE java.util.Date 68 6A 81 01 4B 59 74 19 03 指纹和标志 00 00 无实例变量 78 结束标记 70 无超类 77 08 外部存储、字节的数量 不透明字节 00 00 00 83 E7 4B 7D 80 结束标记 78 name 域的值: String (序列#10) 74 00 0C Carl Cracker secretary 域的值:新对象(序列#11) 73 已有的类(使用序列#4) 71 00 7E 00 04 salary域的值: double 40 E8 6A 00 00 00 00 00 hireDate 域的值:新对象(序列#12) 71 00 7E 00 08 已有的类(使用序列#8) 77 08 外部存储、字节的数量 00 00 00 91 19 97 3D 80 不透明字节 78 结束标记 74 00 0C Harry Hacker name 域的值: String(序列#13) 71 00 7E 00 0B staff[1]:已有的对象(使用序列#11) 73 staff[2]: 新对象(序列#14) 71 00 7E 00 02 已有的类(使用序列#2) 40 E3 88 00 00 00 00 00 salary 域的值: double

hireDay 域的值:新对象(序列#15)

*71 00 7E 66 08*

*已有 使 序列#8*

*77 08*

*外 存储、字节的数*

*ee ee ee 94 6B se*

*不 明字*

*78*

*束标*

*74 00 0B Tony Tester*

*name域 值 String 序列#16*

*7i ee 7E ee 明*

*secretary域 值 已有 对 使 序列#11*

*当然 研究这些编码大概与阅读常用的电话号码簿一样枯 。了 切 文件格式 实不 么 你 图 修改数据来 到不可告人 但是对 流对其所包含 所有对 有详细描 并且 些充 可以 来 构对 和对 数 因此了 它 是大有 处 。*

*你应该记住*

- *对 流 出中包含所有对象的类型和实例域。*
- *每个对 予一个序列号。*
- *・ 同对 复出 将 存储为对 个对 序列号 引 。*

# *2.3.3修改 序列化机制*

*某些实例域是不应 序列化 例如 只对本地方法有意义 存储文件句柄或 口句柄 值 信息在 后 新加 对 或将其传 到其他机器上时 是没有 处 。对对 来 出于提 效 将 些值 存 来是很常 但是并不 在序列化时存储它 们。Java拥有一 很 单 机制来 止 域 序列化 就是将它们标 成transient fi<j<sup>o</sup> 如果 些域属于不可序列化 你也 将它们标 成transient 。 时 域在对 序列化时总是会 。*

*E1<sup>注</sup> 如果一个可序列化 是不可序列化 么它必 有一个可 <sup>无</sup> 参构 器。 下 例子*

> *class Person // Not serializable class Employee extends Person implements Serializable*

*当反序列一个Employee对 时 它 实例域从对 入流中 取 但是Person 实例 域 Person构 器设置。*

*序列化机制为单个 提供了一 定制化 写 为 方式。可序列化的类可以定义 具有下列 名 方法*

*Serial private void readObject ObjectInputStream in throws IOException, ClassNotFoundException; ^Serial private void writeObj ect Obj ectOutputStream out throws IOException;*

*之后 实例域就再也不会 动序列化 取 代之 是 些方法。*

*注意Serial 个注 。对序列化 整 方法并不属于 个接口。因此 无法 使 Override注 器检査 方法 声明。^Serial注 对序列化方法做同 样 检査。到Java 17为止 javac 器 没有 样 检査 但是未来可 会有所改变。* *IntelliJ IDE会 到 个注 。*

*下 是一个典型 定制化 例。在java.awt.geom包中有大 是不可序列化 例如Point-2D.Double 在假 你想 序列化一个LabeledPoint 它存储了一个String和一 个 Point2D.Double。 先 你 将 Point2D.Double域标 成 transient,以 免抛出 NotSeria-LizableException。*

```
public class LabeledPoint implements Serializable
{
   private String label;
   private transient Point2D.Double point;
   I • •
}
```

*在writeObject方法中 我们 先通过调用defaultWriteObject方法写出对 描 和 String域label, 是ObjectOutputStream 中 一个 殊 方法 它只 在可序列化类的 writeObject方法中 。然后 我们使 标准 DataOutput调用写出点 坐标。*

```
private void writeObject(ObjectOutputStream out) throws IOException
{
   out.defaultWriteObject();
   out.writeDouble(point getX());
   out.writeDouble(point.getY());
}
在readObject方法中 我们反 来执 上
private void readObject(ObjectlnputStream in)
      throws IOException, ClassNotFoundException
{
   in.defaultReadObjectO;
   double x = in.readDoubleO;
   double y = in.readDouble();
   point = new Point2D.Double(x, y);
}
```

*另一个例子是HashSet 它提供了 己 readObject和writeObject方法。writeObject 方法并没有将 内 构存储在散列 中 是 接存储容 、 因子、尺寸和各个元 。readObject方法会 回容 和 因子 构建一个新 然后插入各个元 。*

*readObject和writeObject方法只需要保存和加 它们 数据 不关心 数据和任何 其他 信息。*

*Date <sup>使</sup> 了这种方式 它 writeObject方法存储了从" <sup>元</sup>"( <sup>1970</sup>年1月1日)以 来 毫 数 其 存日历数据 数据 构并不会 存储。因此 在2J.2 中 序列化 Date实例包含一个不 明 数据块。*

*0 曹告 就像构 器一样 readObject方法会在只 <sup>了</sup> 分初始化 <sup>对</sup> 上执 操作。 如果在readObject方法 内 在子 中 final方法 么 方法可 会访问到未初始化 数据。*

■ 注释:如果某个可序列化的类定义了下面的域:

@Serial private static final ObjectStreamField[] serialPersistentFields

那么序列化就会使用这些域而不是非瞬时、非静态的域的描述符。还有一个用于在序列化之前设置域值或在反序列化之后读取域值的 API。这个 API 在类演化之后仍想保留其原有布局时会显得很有用。例如,BigDecimal 类使用了这种机制来序列化它的实例,它的序列化的格式其实已经与其实例域的格式不一样了。

除了让序列化机制来保存和恢复对象数据,类还可以定义它自己的机制。为了做到这一点,这个类必须实现 Externalizable 接口,这需要它定义两个方法:

```
public void readExternal(ObjectInput in) throws IOException, ClassNotFoundException;
public void writeExternal(ObjectOutput out) throws IOException;
```

与前面一节描述的 readObject 和 writeObject 不同,这些方法对包括超类数据在内的整个对象的存储和恢复负全责。在写出对象时,序列化机制在输出流中仅仅只是记录该对象所属的类。在读入可外部化的类时,对象输入流将用无参构造器创建一个对象,然后调用 readExternal 方法。

你可以加密数据或者使用比序列化格式更高效的格式。

在下面的示例中, LabeledPixel 类扩展自可序列化的 Point 类, 但是它接管了这个类及其超类的序列化, 其对象的域没有按照标准的序列化格式存储, 所有数据都被放到了一个不透明的块中。

```
public class LabeledPixel extends Point implements Externalizable {
   private String label;
   public LabeledPixel() {} // required for externalizable class
   public void writeExternal(ObjectOutput out) throws IOException {
      out.writeInt((int) getX());
      out.writeInt((int) getY());
      out.writeUTF(label);
   }
   public void readExternal(ObjectInput in)
            throws IOException, ClassNotFoundException {
      int x = in.readInt();
      int y = in.readInt();
      setLocation(x, y);
      label = in.readUTF();
   }
   . . .
}
```

● 警告: readObject 和 writeObject 方法是私有的,并且只能被序列化机制调用。与此不同的是,readExternal 和 writeExternal 方法是公共的。特别是,readExternal 还潜在地允许修改现有对象的状态。

**注释**: 你不能定制枚举和记录的序列化。如果你定义了 readObject/writeObject 或 readExternal/writeExternal 方法,它们并不会用于序列化。

#### 2.3.4 readResolve 和 writeReplace 方法

在序列化和反序列化时,对象 ID 会造成麻烦,你必须加倍当心,这通常会在实现单例和实例数量有限的类时发生。

如果你使用 Java 语言的 enum 结构,那么你就不必担心序列化,它能够正常工作。但是,假设你在维护遗留代码,其中包含下面这样的枚举类型:

```
public class Orientation
{
  public static final Orientation HORIZONTAL = new Orientation(1);
  public static final Orientation VERTICAL = new Orientation(2);
  private int value;
  private Orientation(int v)
  {
     value = v;
  }
}
```

这种风格在枚举被添加到 Java 语言中之前是很普遍的。注意,其构造器是私有的。因此,不可能创建出超出 Orientation. HORIZONTAL 和 Orientation. VERTICAL 之外的对象。特别是,你可以使用 == 操作符来测试对象的等同性:

```
if (orientation == Orientation.HORIZONTAL) . . .
```

默认的序列化机制是不适用的。假设我们写出一个 Orientation 类型的值,并再次将其读回:

```
Orientation original = Orientation.HORIZONTAL;
ObjectOutputStream out = . . .;
out.write(original);
out.close();
ObjectInputStream in = . . .;
var saved = (Orientation) in.read();

现在,下面的测试
```

if (saved == Orientation.HORIZONTAL) . . .

将失败。事实上, saved 的值是 Orientation 类型的一个全新的对象, 它与任何预定义的常量都不等同。即使构造器是私有的, 序列化机制也可以创建新的对象!

为了解决这个问题,你需要定义另外一种称为 readResolve 的特殊序列化方法。如果定义了 readResolve 方法,在对象被序列化之后就会调用它。它必须返回一个对象,而该对象之后会成为 readObject 方法的返回值。在上面的情况中,readResolve 方法将检查 value 域并返回恰当的枚举常量:

```
@Serial private Object readResolve() throws ObjectStreamException
{
   if (value == 1) return Orientation.HORIZONTAL;
   else if (value == 2) return Orientation.VERTICAL;
   else throw new ObjectStreamException(); // this shouldn't happen
}
```

☑ 提示:在使用单例类时,你也必须当心不要让反序列化产生第2个实例。使用枚举可以避免这个问题:

```
public enum MySingleton
{
   INSTANCE;
   MySingleton() { . . . } // automatically private
   // instance fields
   // methods
}
```

因为枚举会被正确反序列化,所以你可以确保只有一个 MySingleton. INSTANCE。

有时, readResolve 方法与另一个特殊的方法结合使用:

@Serial private Object writeReplace() throws ObjectStreamException

writeReplace 会产生一个对象,将其写出到对象流中,而不是将当前对象写出到对象流中。这个替代对象必须是可序列化或可外部化的。当读取该对象流时,这个替代对象会被反序列化,其 readResolve 方法会被调用以重新创建出最初的对象。

**注释:** 不同于 readObject 和 writeObject 方法必须是 private 的或者 readExternal/write-External 方法必须是 public 的,readResolve 和 writeReplace 方法可以有任意的访问修饰符。

下面的示例展示了这种机制。ColoredPoint 的 writeReplace 方法会产生一个嵌套类 Ser 的替代对象。为了方便,这个示例使用了记录。替代类的 readResolve 方法会重建最初的 ColoredPoint 对象。

```
public class ColoredPoint implements Serializable
{
   private Color color;
   private Point location;

   public ColoredPoint(Color color, int x, int y)
   {
      this.color = color;
      this.location = new Point(x, y);
   }

   @Serial private Object writeReplace() throws ObjectStreamException
   {
      return new Ser(color.getRGB(), location.x, location.y);
   }

   private record Ser(int rgba, int x, int y) implements Serializable
   {
```

```
(^Serial private Object readResolve() throws ObjectStreamException
        {
            return new ColoredPoint(new Color(rgba), x, y);
        }
    }
}
```

*为什么 么 烦 序列化将存储2个对象而不是3个整数。你可以 readExternaUwriteExternal方法来实 保存同样 内容 但是 些方法必 是public 。*

*LocalDate 以及在java.time包中 其他 使 了 。因此 个序列化 例 使 是Date对 因为我并不想 力去 对 流中为什么存在Ser对 。*

*注 <sup>与</sup> readObj ect/writeObj ect 方法不同 readResolve 和 writeReplace 方法不必是 private 。 5*

# *2.3.5 <sup>本</sup>*

*如果使 序列化来保存对 就 在 序演化时会有什么 。例如 1.1 本 可以 人旧文件吗 仍旧使 1.0 本 户可以 人新 本产 文件吗 显然 如果对 文件可以处 演化 它正是我们想 。*

*乍一 好像是不可 。无论类的定义产 了什么样 变化 它 SHA指纹都会 跟着变化 我们 对 入流将拒 入具有不同指 对 。但是 可以 明它 对其早期 本保持兼容 想 样做 就必 先 得 个 早期 本 指 。我们可以 使 JDK中 单机 序serialver来 得 个数字 例如 下 命令*

*serialver serial.Employee*

# *将会打印出*

```
serial.Employee: static final long serialVersionUID = 8367346051156850807L;
```

*个 所有 新 本 必 把serialVersionUID常 定义为与最初 本 指 同。*

```
class Employee implements Serializable // version 1.1
{
   • ft
   ^Serial public static final long serialVersionUID = 8367346051156850807L;
}
```

*如果一个 具有名为serialVersionUID 态数据成员 它就不再 人工 指 , 只 接使 个值。*

*一旦 个 态数据成员 于某个 内 么序列化 就可以 入 个 对 不同 本。*

*如果 个 只有方法产 了变化 么在 人新对 数据时是不会有任何 。但 是 如果实例域产 了变化 么就可 会有 。例如 旧文件对 可 比 序中 对 具有更多或更少 实例域 或 实例域 型可 有所不同。在 些情况中 对象输入流将 尽力将流对 换成 个 当前 本。*

*对 入流会将 个 当前 本 实例域与 序列化 本中 实例域 比 当*

然,对象流只会考虑非瞬时和非静态的实例域。如果这两部分实例域之间名字匹配而类型不匹配,那么对象输入流不会尝试将一种类型转换成另一种类型,因为这两个对象不兼容;如果被序列化的对象具有在当前版本中所没有的实例域,那么对象输入流会忽略这些额外的数据;如果当前版本具有在被序列化的对象中所没有的实例域,那么这些新添加的域将被设置成它们的默认值(如果是对象则是 null,如果是数字则为 0,如果是 boolean 值则是 false)。

下面是一个示例: 假设我们已经用雇员类的最初版本(1.0)在磁盘上保存了大量的雇员记录,现在我们在 Employee 类中添加了称为 department 的实例域,从而将其演化到了 2.0 版本。图 2-7 展示了将 1.0 版的对象读入使用 2.0 版对象的程序中的情形,可以看到 department 域被设置成了 null。图 2-8 展示了相反的情况:一个使用 1.0 版对象的程序读入了 2.0 版的对象,可以看到额外的 department 域被忽略。

这种处理是安全的吗?视情况而定。丢掉实例域看起来是无害的,因为接收者仍旧拥有它知道如何处理的所有数据,但是将实例域设置为 null 却有可能并不那么安全。许多类都费尽心思地在其所有的构造器中将所有的实例域都初始化为非 null 的值,以使得其各个方法都不必去处理 null 数据。因此,这个问题取决于类的设计者是否能够在 readObject 方法中实现额外的代码去订正版本不兼容问题,或者是否能够确保所有的方法在处理 null 数据时都足够健壮。

![](_page_98_Figure_5.jpeg)

图 2-7 读人具有较少实例域的对象

![](_page_98_Figure_7.jpeg)

图 2-8 读人具有较多实例域的对象

- *提 在将serialVersionUID域添加到 中之前 需要问问自己为什么要让这个 是 可序列化 。如果序列化只是 于 期持久化 例如在应 服务器中 分布式方法 么就不 关心 本机制和serialVersionUID。如果 巧 扩展一个可序列化 但是又从来没想 持久化 扩展 任何实例 么同样不 关心它们。如 果IDE总是报有关此 烦人 告消息 么可以修改IDE偏好 将它们关 <sup>或</sup> 添加@SuppressWarnings( "serial")<sup>注</sup> 。 样做比添加serialVersionUID 更安 全 因为也 后 我们会忘 修改serialVersionUID*
- *S 注 枚举和 录会忽 serialVersionUID域。枚举总是会有一个值为0L serialVersionUDo 你可以为 录声明一个serialVersionUID,但是在反序列化时并不 匹 些ID*
- *Q <sup>注</sup> 在本 <sup>你</sup> 到了 入器 <sup>入</sup> 本中具有对 流中不存在 实例城时所发 情况。 有可 在 演化 中在 中添加了新实例域 然后使 新 本 入器 入 对 流中 实例城并未 。默认情况下 些实例城会 成6/nuU值 可 会导 处于不安全 态。 可以 定义初始化 方法来 此*

*^Serial private void readObjectNoDataO throws ObjectStreamException*

*方法应 么将上 域 为与无参构 器 态 同 么抛出InvalidObject-Exception异常。它应 只在 常 情况下才会 即 入 对 流包含 子 实 例 失 数据。*

# *2.3.6为克 <sup>使</sup> 序列化*

*序列化机制有一 很有趣的用法 即提供了一 克 对象的简便 径 只 对应的类是 可序列化 即可。其做法很 单 接将对 序列化到 出流中 然后将其 回。 样产 新对 是对 有对 一个深拷 (deep copy) 在此过程中 我们不必将对 写出到文 件中 因为可以 ByteArrayOutputStream将数据保存到字 数 中。*

*正如 序清单2«4所 想得到done方法 只 扩展SerialCloneable 样就完事了。*

## *序清单 2-4 serialClone/SerialCloneTest.java*

```
1 package serialClone;
2
3 /"
4 * ^version 1.22 2018-05-91
5 ^author Cay Horstmann
6 /
7
8 import java.io.
9 import java.time.*;
le
n public class SerialCloneTest
u {
13 public static void main(String[] args) throws CloneNotSupportedException
```

```
14
15
         var harry = new Employee("Harry Hacker", 35000, 1989, 10, 1);
         // clone harry
16
         var harry2 = (Employee) harry.clone();
17
18
         // mutate harry
19
         harry.raiseSalary(10);
28
21
         // now harry and the clone are different
22
         System.out.println(harry);
23
         System.out.println(harry2);
24
25
26
27
28
    * A class whose clone method uses serialization.
29
30
   class SerialCloneable implements Cloneable, Serializable
31
32
      public Object clone() throws CloneNotSupportedException
33
34
      {
         try {
35
            // save the object to a byte array
36
            var bout = new ByteArrayOutputStream();
37
            try (var out = new ObjectOutputStream(bout))
38
            {
39
                out.writeObject(this);
48
            }
41
42
            // read a clone of the object from the byte array
43
            try (var bin = new ByteArrayInputStream(bout.toByteArray()))
44
45
                var in = new ObjectInputStream(bin);
46
                return in.readObject();
47
            }
48
         }
49
         catch (IOException | ClassNotFoundException e)
SA
51
            var e2 = new CloneNotSupportedException();
52
            e2.initCause(e);
53
            throw e2;
54
55
56
57
58
59
    * The familiar Employee class, redefined to extend the
    * SerialCloneable class.
61
62
   class Employee extends SerialCloneable
63
   {
64
      private String name;
65
66
      private double salary;
      private LocalDate hireDay;
67
68
```

```
public Employee(String n, double s, int year, int month, int day)
      {
78
71
          name = n;
          salary = s;
72
73
          hireDay = LocalDate.of(year, month, day);
74
75
      public String getName()
76
77
          return name;
78
79
88
      public double getSalary()
81
82
          return salary;
83
84
85
      public LocalDate getHireDay()
86
87
          return hireDay;
88
89
90
91
          Raises the salary of this employee.
92
          @param byPercent the percentage of the raise
93
94
      public void raiseSalary(double byPercent)
95
96
          double raise = salary * byPercent / 100;
97
98
          salary += raise;
99
100
      public String toString()
101
102
          return getClass().getName()
             + "[name=" + name
184
             + ", salary=" + salary
105
             + ", hireDay=" + hireDay
196
             + "]";
187
108
109 }
```

我们应该当心这个方法,尽管它很灵巧,但是通常会比显式地构建新对象并复制或克隆 实例域的克隆方法慢得多。

# 2.3.7 反序列化和安全

在可序列化类的反序列化过程中,对象是在没有调用该类的任何构造器的情况下创建出来的,即使该类有无参构造器,也不会调用它。对象的域的值会直接用对象输入流中的值设置。

直 注释: 对于可序列化记录,反序列化会调用标准构造器,传递给它从对象输入流中获取的各个组成部分中的值。(因此,记录中的循环引用将无法恢复。)

绕过构造器是一种安全风险,因为这使得攻击者可以精心设计一些字节,用来描述永远都不可能构造出来的无效对象。例如,假设 Employee 构造器会在用负数表示的薪水调用它时抛出异常,我们自然就会认为不会有任何 Employee 对象的薪水为负数。但是,正如在前一节中所看到的,审视序列化对象的字节并修改其中的内容并非难事。通过这种方式就可以编造出薪水为负数的雇员,然后再将其反序列化。

可序列化类可以有选择地实现 ObjectInputValidation 接口,并定义 validateObject 方法来检查其对象是否被正确地反序列化。例如, Employee 类可以检查薪水不能为负:

```
public void validateObject() throws InvalidObjectException
{
    System.out.println("validateObject");
    if (salary < θ)
        throw new InvalidObjectException("salary < θ");
}
遗憾的是,这个方法不会被自动调用。要想调用它,你必须还要提供下面的方法:
@Serial private void readObject(ObjectInputStream in)
```

然后,这个对象才会被调度进行验证,当这个对象及所有依赖对象都被加载之后, validateObject 方法才会被调用。第 2 个参数是用来指定优先级的,具有高优先级的验证请求会先被执行。

还有一些其他的安全风险。对手可以创建出一些数据结构,它们十分消耗资源,足以让虚拟机崩溃。更险恶的是,任何在类路径上的类都可以被反序列化。黑客可以采用迂回策略,将多个"小工具链"和操作序列串在一起,它们看起来就像是各式各样的实用类,但是它们使用了反射机制,并且最终以用黑客选择的字符串调用像 Runtime.exec 这样的方法而结束。

任何通过网络连接从不可信的来源接收序列化数据的应用程序都很容易遭受此类攻击。例如,有些服务器会序列化会话(session)数据,并反序列化所有在 HTTP 会话 cookie 中返回的数据。

你应该避免对来自不可信来源的数据进行反序列化的情况。在会话数据的例子中,服务 器应该对数据签名并且只对具有有效签名的数据进行反序列化。

JEP 290 和 415 提供了一种序列化过滤器机制,用来加固应用程序,以免受此类攻击。 过滤器可以观察到被反序列化的类的名字,以及若干项指标(流尺寸、数组尺寸、引用总数、 最长的引用链等)。过滤器可以基于这些数据决定是否要放弃反序列化。

在形式最简单的过滤器中,我们只需要提供一种描述有效和无效类的模式。例如,如果按照下面的方式运行序列化演示样例:

java -Djdk.serialFilter='serial.\*;java.\*\*;!\*' serial.ObjectStreamTest

那么这些对象就会被加载。这里的过滤器允许所有在 serial 包中的类和所有名字以 java 开头的包中的类序列化,但是其他所有类都不能序列化。如果不允许 java.\*\* 或至少 java.util. Date, 那么反序列化将失败。

你可以将过滤器模式放置到配置文件中,并且可以指定多个用于不同目的的过滤器。你还可以实现自己的过滤器。详情请参考 https://docs.oracle.com/en/java/javase/17/core/serial-ization-filtering1.html。

# 2.4 操作文件

你已经学习了如何从文件中读写数据,然而文件管理的内涵远远比读写要广。Path 接口和 Files 类封装了在用户机器上处理文件系统所需的所有功能。例如,Files 类可以用来移除或重命名文件,或者查询文件最后被修改的时间。换句话说,输入/输出流类关心的是文件的内容,而我们在此处要讨论的类关心的是文件在磁盘上的存储。

Path 接口和 Files 类是在 Java 7 中新添加进来的,它们用起来比自 JDK 1.0 以来就一直使用的 File 类要方便得多。我们认为这两个类会在 Java 程序员中流行起来,因此在这里做深度讨论。

#### 2.4.1 Path

Path (路径)表示的是一个目录名序列,其后还可以跟着一个文件名。路径中的第一个部件可以是根部件,例如/或 C:\,而允许访问的根部件取决于文件系统。以根部件开始的路径是绝对路径;否则,就是相对路径。例如,我们要分别创建一个绝对路径和一个相对路径;其中,对于绝对路径,我们假设计算机运行的是类 UNIX 的文件系统:

```
Path absolute = Path. of ("/home", "harry");
Path relative = Path. of ("myprog", "conf", "user.properties");
```

静态的 Paths.get 方法接受一个或多个字符串,并将它们用默认文件系统的路径分隔符(类 UNIX 文件系统是/, Windows 是\) 连接起来。然后它解析连接起来的结果,如果其表示的不是给定文件系统中的合法路径,那么就抛出 InvalidPathException 异常。这个连接起来的结果就是一个 Path 对象。

get 方法可以获取包含多个部件的单个字符串,例如,可以像下面这样从配置文件中读取路径:

```
String baseDir = props.getProperty("base.dir");
  // May be a string such as /opt/myprog or c:\Program Files\myprog
Path basePath = Path.of (baseDir); // OK that baseDir has separators
```

註釋: 路径不必对应着某个实际存在的文件,它仅仅是一个抽象的名字序列。在接下来的小节中将会看到,当你想要创建文件时,首先要创建一个路径,然后才调用方法去创建对应的文件。

组合或解析路径是司空见惯的操作,调用 p. resolve(q) 将按照下列规则返回一个路径:

- 如果 q 是绝对路径,则结果就是 q。
- 否则,根据文件系统的规则,将"p后面跟着q"作为结果。

例如,假设你的应用系统需要查找相对于给定基目录的工作目录,其中基目录是从配置文件中读取的,就像前一个例子一样。

```
Path workRelative = Path.of("work");
Path workPath = basePath.resolve(workRelative);
```

resolve 方法有一种快捷方式,它接受一个字符串而不是路径:

Path workPath = basePath.resolve("work");

还有一个很方便的方法 resolveSibling,它通过解析指定路径的父路径产生其兄弟路径。例如,如果 workPath 是 /opt/myapp/work,那么下面的调用

Path tempPath = workPath.resolveSibling("temp");

将创建 /opt/myapp/temp。

resolve 的对立面是 relativize, 即调用 p. relativize(r) 将产生路径 q, 而对 q 进行解析的结果正是 r。例如,以"/home/harry"为目标对"/home/fred/input.txt"进行相对化操作,会产生"../fred/input.txt", 其中,我们假设..表示文件系统中的父目录。

normalize 方法将移除所有冗余的.和..部件(或者文件系统认为冗余的所有部件)。例如,规范化/home/harry/../fred/./input.txt将产生/home/fred/input.txt。

toAbsolutePath 方法将产生给定路径的绝对路径,该绝对路径从根部件开始,例如 /home/fred/input.txt 或 c:\Users\fred\input.txt。

Path 类有许多有用的方法用来将路径断开。下面的代码示例展示了其中部分最有用的方法:

Path p = Path.of("/home", "fred", "myprog.properties");

Path parent = p.getParent(); // the path /home/fred

Path file = p.getFileName(); // the path myprog.properties

Path root = p.getRoot(); // the path /

正如你已经在卷 I 中看到的,还可以从 Path 对象中构建 Scanner 对象:

var in = new Scanner(Path.of("/home/fred/input.txt"));

i 注释: 偶尔, 你可能需要与遗留系统的 API 交互, 它们使用的是 File 类而不是 Path 接口。Path 接口有一个 to File 方法, 而 File 类有一个 to Path 方法。

# API java.nio.file.Paths

static Path get(String first, String... more)
 通过连接给定的字符串创建一个路径。

## API java.nio.file.Path

- Path resolve(Path other)
- Path resolve(String other)
   如果 other 是绝对路径,那么就返回 other;否则,返回通过连接 this 和 other 获得的路径。
- Path resolveSibling(Path other)
- Path resolveSibling(String other)
   如果 other 是绝对路径,那么就返回 other;否则,返回通过连接 this 的父路径和 other 获得的路径。
- Path relativize(Path other)
   返回用 this 进行解析,相对于 other 的相对路径。

- Path normalize()
   移除诸如,和,等冗余的路径元素。
- Path toAbsolutePath()
   返回与该路径等价的绝对路径。
- Path getParent()
   返回父路径,或者在该路径没有父路径时,返回 null。
- Path getFileName() 返回该路径的最后一个部件,或者在该路径没有任何部件时,返回 null。
- Path getRoot()
   返回该路径的根部件,或者在该路径没有任何根部件时,返回 null。
- toFile()
   从该路径中创建一个 File 对象。

#### API java.io.File 1.0

Path toPath() 7
 从该文件中创建一个 Path 对象。

#### 2.4.2 读写文件

Files 类可以使得普通文件操作变得快捷。例如,可以用下面的方式很容易地将文件的 所有内容读入字节数组、字符串,以及由行构成的列表或由行构成的流中:

```
byte[] bytes = Files.readAllBytes(path);
String content = Files.readString(path, charset);
List<String> lines = Files.readAllLines(path, charset);
Stream<String> lineStream = Files.lines(path, charset);
```

相反,对于写出,可以调用:

Files.write(path, bytes);
Files.writeString(path, content, charset);
Path.write(path, lines, charset);

向指定文件追加内容,可以调用:

Files.write(path, content, charset, StandardOpenOption.APPEND);

下面的调用:

long pos = Files.mismatch(path1, path2);

将产生两个文件的内容中第1个不相同字节的位置。

为了获取文件中的 MIME 类型 (例如"text/html"或"image/png"),可以调用

String mimeType = Files.probeContentType(path);

其确切行为取决于 Java 的具体实现。每种实现都有一个 FileTypeDetector 实例的集合,它们会按照未指定的顺序尝试进行获取。每个探测器都可能会检查文件的扩展名、OS 相关的元数据和文件内容的前几个字节。

下面的方法使你可以与使用了经典的输入/输出流或者读入器/写出器的 API 进行交互:

InputStream in = Files.newInputStream(path);
OutputStream out = Files.newOutputStream(path);
Reader in = Files.newBufferedReader(path, charset);
Writer out = Files.newBufferedWriter(path, charset);

这些便捷方法可以将你从处理 FileInputStream、FileOutputStream、BufferedReader 和 BufferedWriter 的繁复操作中解脱出来。

#### API java.nio.file.Files

- static byte[] readAllBytes(Path path)
- static String readString(Path path, Charset charset)
- static List<String> readAllLines(Path path, Charset charset)
   读入文件的内容。
- static Path write(Path path, byte[] contents, OpenOption... options)
- static Path write(Path path, String contents, Charset charset, OpenOption... options)
- static Path writeString(Path path, CharSequence contents, Charset cs, OpenOption... options) 11
- static Path write(Path path, Iterable<? extends CharSequence> contents, OpenOption options) 将给定内容写出到文件中,并返回 path。
- static long mismatch(Path path, Path path2) 12 返回两个文件的内容中第1个不相同的字节的位置。
- static String probeContentType(Path path) 12
   返回针对文件内容的 MIME 类型的各种已安装的文件类型探测器中的最佳匹配,或者在无法确定类型时返回 null。
- static InputStream newInputStream(Path path, OpenOption... options)
- static OutputStream newOutputStream(Path path, OpenOption... options)
- static BufferedReader newBufferedReader(Path path, Charset charset)
- static BufferedWriter newBufferedWriter(Path path, Charset charset, OpenOption... options)
   打开一个文件,用于读入或写出。

# 2.4.3 创建文件和目录

创建新目录可以调用

Files.createDirectory(path);

其中,路径中除最后一个部件外,其他部分都必须是已存在的。要创建路径中的中间目录,应该使用

Files.createDirectories(path);

可以使用下面的语句创建一个空文件:

Files.createFile(path);

如果文件已经存在了,那么这个调用就会抛出异常。检查文件是否存在和创建文件是原子性的,如果文件不存在,该文件就会被创建,并且其他程序在此过程中是无法执行文件创建操作的。

有些便捷方法可以用来在给定位置或者系统指定位置创建临时文件或临时目录:

Path newPath = Files.createTempFile(dir, prefix, suffix);

Path newPath = Files.createTempFile(prefix, suffix);

Path newPath = Files.createTempDirectory(dir, prefix);

Path newPath = Files.createTempDirectory(prefix);

其中, dir 是一个 Path 对象, prefix 和 suffix 是可以为 null 的字符串。例如, 调用 Files. createTempFile(null, ".txt") 可能会返回一个像 /tmp/1234405522364837194.txt 这样的路径。

在创建文件或目录时,可以指定属性,例如文件的拥有者和权限。但是,指定属性的细节取决于文件系统,本书在此不做讨论。

#### API java.nio.file.Files

- static Path createFile(Path path, FileAttribute<?>... attrs)
- static Path createDirectory(Path path, FileAttribute<?>... attrs)
- static Path createDirectories(Path path, FileAttribute<?>... attrs) 创建一个文件或目录, createDirectories 方法还会创建路径中所有的中间目录。
- static Path createTempFile(String prefix, String suffix, FileAttribute<?>... attrs)
- static Path createTempFile(Path parentDir, String prefix, String suffix, FileAttribute<?>...
   attrs)
- static Path createTempDirectory(String prefix, FileAttribute<?>... attrs)
- static Path createTempDirectory(Path parentDir, String prefix, FileAttribute<?>... attrs) 在适合临时文件的位置,或者在给定的父目录中,创建一个临时文件或目录。返回所创建的文件或目录的路径。

## 2.4.4 复制、移动和删除文件

将文件从一个位置复制到另一个位置可以直接调用

Files.copy(fromPath, toPath);

移动文件(即复制并删除原文件)可以调用

Files.move(fromPath, toPath);

如果目标路径已经存在,那么复制或移动将失败。如果想要覆盖已有的目标路径,可以使用 REPLACE\_EXISTING 选项。如果想要复制所有的文件属性,可以使用 COPY\_ATTRIBUTES 选项。也可以像下面这样同时选择这两个选项:

Files.copy(fromPath, toPath, StandardCopyOption.REPLACE\_EXISTING, 

你可以将移动操作定义为原子性的,这样就可以保证要么移动操作成功完成,要么源文件继续保持在原来位置。具体可以使用 ATOMIC MOVE 选项来实现:

Files.move(fromPath, toPath, StandardCopyOption.ATOMIC\_MOVE);

你还可以将一个输入流复制到 Path 中,这表示想要将该输入流存储到硬盘上。类似地,你可以将一个 Path 复制到输出流中。可以使用下面的调用:

Files.copy(inputStream, toPath);
Files.copy(fromPath, outputStream);

至于其他对 copy 的调用,可以根据需要提供相应的复制选项。

最后, 删除文件可以调用:

Files.delete(path);

如果要删除的文件不存在,这个方法就会抛出异常。因此,可转而使用下面的方法:

boolean deleted = Files.deleteIfExists(path);

该删除方法还可以用来移除空目录。

请查阅表 2-4 以了解对文件操作而言可用的选项。

| 选项                 | 描述                                                            |  |
|--------------------|---------------------------------------------------------------|--|
| StandardOpenOption | 与 newBufferedWriter、newInputStream、newOutputStream、write 一起使用 |  |
| READ               | 用于读取而打开                                                       |  |
| WRITE              | 用于写人而打开                                                       |  |
| APPEND             | 如果用于写人而打开, 那么在文件末尾追加                                          |  |
| TRUNCATE_EXISTING  | 如果用于写人而打开, 那么移除已有内容                                           |  |
| CREATE_NEW         | 创建新文件并且在文件已存在的情况下会创建失败                                        |  |
| CREATE             | 自动在文件不存在的情况下创建新文件                                             |  |
| DELETE_ON_CLOSE    | 当文件被关闭时,尽"可能"地删除该文件                                           |  |
| SPARSE             | 给文件系统一个提示,表示该文件是稀疏的                                           |  |
| DSYNC 或 SYNC       | 要求对文件数据   数据和元数据的每次更新都必须同步地写入到存储设备中                           |  |
| StandardCopyOption | 与 copy 和 move 一起使用                                            |  |
| ATOMIC_MOVE        | 原子性地移动文件                                                      |  |
| COPY_ATTRIBUTES    | 复制文件的属性                                                       |  |
| REPLACE_EXISTING   | 如果目标已存在,则替换它                                                  |  |
| LinkOption         | 与上面所有方法以及 exists、isDirectory、isRegularFile 等一起使用              |  |
| NOFOLLOW_LINKS     | 不要跟踪符号链接                                                      |  |
| FileVisitOption    | 与 find、walk、walkFileTree 一起使用                                 |  |
| FOLLOW_LINKS       | 跟踪符号链接                                                        |  |

表 2-4 用于文件操作的标准选项

#### API java.nio.file.Files 7

- static Path copy(Path from, Path to, CopyOption... options)
- static Path move(Path from, Path to, CopyOption... options)
   将 from 复制或移动到给定位置,并返回 to。
- static long copy(InputStream from, Path to, CopyOption... options)

- static long copy(Path from, OutputStream to, CopyOption... options)
  从输入流复制到文件中,或者从文件复制到输出流中,返回复制的字节数。
- static void delete(Path path)
- static boolean deleteIfExists(Path path)
   删除给定文件或空目录。第一个方法在文件或目录不存在情况下抛出异常,而第二个方法在这种情况下会返回 false。

#### 2.4.5 获取文件信息

下面的静态方法都将返回一个 boolean 值,表示检查路径的某个属性的结果:

- exists
- isHidden
- isReadable, isWritable, isExecutable
- isRegularFile, isDirectory, isSymbolicLink

size 方法将返回文件的字节数:

long fileSize = Files.size(path);

getOwner 方法将文件的拥有者作为 java.nio.file.attribute.UserPrincipal 的一个实例返回。 所有的文件系统都会报告一个基本属性集,它们被封装在 BasicFileAttributes 接口中, 这些属性与上述信息有部分重叠。基本文件属性包括:

- 创建文件、最后一次访问以及最后一次修改文件的时间,这些时间都表示成 java.nio. file.attribute.FileTime。
- 文件是常规文件、目录还是符号链接,抑或这三者都不是。
- 文件尺寸。
- 文件主键,这是某种类的对象,具体所属类与文件系统相关,有可能是文件的唯一标识符,也可能不是。

要获取这些属性, 可以调用

BasicFileAttributes attributes = Files.readAttributes(path, BasicFileAttributes.class);

如果你了解到用户的文件系统兼容 POSIX, 那么你可以获取一个 PosixFileAttributes 实例:
PosixFileAttributes attributes = Files.readAttributes(path, PosixFileAttributes.class);

然后从中找到组拥有老 以及文件的拥有老 组和访问权限 我们不会详

然后从中找到组拥有者,以及文件的拥有者、组和访问权限。我们不会详细讨论其细节,因为这种信息中很多内容在操作系统之间并不具备可移植性。

#### API java.nio.file.Files

- static boolean exists(Path path)
- static boolean isHidden(Path path)
- static boolean isReadable(Path path)
- static boolean isWritable(Path path)
- static boolean isExecutable(Path path)

- static boolean isRegularFile(Path path)
- static boolean isDirectory(Path path)
- static boolean isSymbolicLink(Path path)
   检查由路径指定的文件的给定属性。
- static long size(Path path)
   获取文件按字节数度量的尺寸。
- A readAttributes(Path path, Class<A> type, LinkOption... options)
   读取类型为 A 的文件属性。

#### API java.nio.file.attribute.BasicFileAttributes

- FileTime creationTime()
- FileTime lastAccessTime()
- FileTime lastModifiedTime()
- boolean isRegularFile()
- boolean isDirectory()
- boolean isSymbolicLink()
- long size()
- Object fileKey()
   获取所请求的属性。

java/nio/DirectCharBufferU.java

java/nio/MappedByteBuffer.java

java/nio/ByteBufferAsShortBufferRL.java

#### 2.4.6 访问目录中的项

静态的 Files.list 方法会返回一个可以读取目录中各个项的 Stream<Path>对象。目录是被惰性读取的,这使得处理具有大量项的目录可以变得更高效。

因为读取目录涉及需要关闭的系统资源, 所以应该使用 try 块:

```
try (Stream<Path> entries = Files.list(pathToDirectory))
{

list 方法不会进入子目录。为了处理目录中的所有子目录,需要使用 File.walk 方法。

try (Stream<Path> entries = Files.walk(pathToRoot))
{

// Contains all descendants, visited in depth-first order
}

下面是解压后的 src.zip 树的遍历样例:
java
java/nio
```

```
java/nio/ByteBufferAsDoubleBufferB.java
java/nio/charset
java/nio/charset/CoderMalfunctionError.java
java/nio/charset/CharsetDecoder.java
java/nio/charset/UnsupportedCharsetException.java
java/nio/charset/spi
java/nio/charset/spi/CharsetProvider.java
java/nio/charset/StandardCharsets.java
java/nio/charset/Charset.java
java/nio/charset/CoderResult.java
java/nio/HeapFloatBufferR.java
```

正如你所见,无论何时,只要遍历的项是目录,那么在继续访问它的兄弟项之前,会先进人它。

可以通过调用 File.walk(pathToRoot, depth)来限制想要访问的树的深度。两种 walk 方法都具有 FileVisitOption... 的可变长参数,但是你只能提供一种选项——FOLLOW\_LINKS,即跟踪符号链接。

i 注释:如果要过滤 walk 返回的路径,并且过滤标准涉及与目录存储相关的文件属性,例如尺寸、创建时间和类型 (文件、目录、符号链接),那么应该使用 find 方法来替代 walk 方法。可以用某个谓词函数来调用这个方法,该函数接受一个路径和一个 BasicFileAttributes 对象。这样做唯一的优势就是效率高。因为路径总是会被读入,所以这些属性很容易获取。

这段代码使用了 Files.walk 方法来将一个目录复制到另一个目录:

```
Files.walk(source).forEach(p ->
{
    try
    {
        Path q = target.resolve(source.relativize(p));
        if (Files.isDirectory(p))
            Files.createDirectory(q);
        else
            Files.copy(p, q);
    }
    catch (IOException ex)
    {
        throw new UncheckedIOException(ex);
    }
});
```

遗憾的是,你无法很容易地使用 Files.walk 方法来删除目录树,因为你必须在删除父目录之前先删除子目录。下一节将展示如何克服此问题。

#### 2.4.7 使用目录流

正如在前一节中所看到的, Files.walk 方法会产生一个可以遍历目录中所有子孙的 Stream<Path>对象。有时,需要对遍历过程进行更加细粒度的控制。在这种情况下,应该使

用 Files.newDirectoryStream 对象,它会产生一个 DirectoryStream。注意,它不是 java.util. stream.Stream 的子接口,而是专门用于目录遍历的接口。它是 Iterable 的子接口,因此可以在增强的 for 循环中使用目录流。下面是其使用模式:

```
try (DirectoryStream<Path> entries = Files.newDirectoryStream(dir))
{
   for (Path entry : entries)
        Process entries
}
```

带资源的 try 语句块用来确保目录流可以被正确关闭。访问目录中的项并没有具体的顺序。可以用 glob 模式来过滤文件:

try (DirectoryStream<Path> entries = Files.newDirectoryStream(dir, "\*.java"))

表 2-5 展示了所有的 glob 模式。

| A L O GIOD DESC |                                       |                                                 |
|-----------------|---------------------------------------|-------------------------------------------------|
| 模 式             | 描述                                    | 示 例                                             |
| *               | 匹配路径组成部分中 0 个或多个字符                    | *.java 匹配当前目录中的所有 Java 文件                       |
| **              | 匹配跨目录边界的 0 个或多个字符                     | **.java 匹配在所有子目录中的 Java 文件                      |
| ?               | 匹配一个字符                                | ????.java 匹配所有四个字符的 Java 文件(不包括扩展名)             |
| []              | 匹配一个字符集合,可以使用连线符<br>[0-9] 和取反符 [!0-9] | Test[0-9A-F].java 匹配 Testx.java, 其中 x 是一个十六进制数字 |
| {}              | 匹配由逗号隔开的多个可选项之一                       | *.{java,class} 匹配所有的 Java 文件和类文件                |
| 1               | 转义上述任意模式中的字符以及\字符                     | *\** 匹配所有文件名中包含*的文件                             |

表 2-5 glob 模式

● 警告:如果使用 Windows 的 glob 语法,则必须对反斜杠转义两次:一次为 glob 语法转义,一次为 Java 字符串转义。例如 Files.newDirectoryStream(dir, "C:\\\")。

如果想要访问某个目录的所有子孙成员,可以转而调用 walkFileTree 方法,并向其传递一个 FileVisitor 类型的对象,这个对象会在下列时刻收到通知:

- 在遇到一个文件或目录时: FileVisitResult visitFile(T path, BasicFileAttributes attrs)
- 在一个目录被处理前: FileVisitResult preVisitDirectory(T dir, IOException ex)
- 在一个目录被处理后: FileVisitResult postVisitDirectory(T dir, IOException ex)
- 在试图访问文件或目录时发生错误,例如没有权限打开目录: FileVisitResult visitFileFailed(path, IOException)

对于上述每种情况,都可以指定是否希望执行下面的操作:

- 继续访问下一个文件: FileVisitResult.CONTINUE
- 继续访问,但是不再访问这个目录下的任何项了: FileVisitResult.SKIP\_SUBTREE
- 继续访问,但是不再访问这个文件的兄弟文件(和该文件在同一个目录下的文件)了: FileVisitResult.SKIP SIBLINGS
- 终止访问: FileVisitResult.TERMINATE

当有任何方法抛出异常时,就会终止访问,而这个异常会从 walkFileTree 方法中抛出。

*0 <sup>注</sup> FileVisitor接口是泛化 <sup>型</sup> 但是你不太可 会使 FileVisitor<Path>之外 东 。walkFileTree方法可以接受FileVisitor<? Super Path> 型 参数 但是Path 并没有多少超类型。*

*便捷 SimpleFileVisitor 实 了 FileVisitor 接口 但是其 visitFileFailed 方法之外 所有方法并不做任何处理而是 接继续访问 visitFileFailed方法会抛出 失 导 异常 并 止 。*

*例如 下 代 展 了如何打印出 定 录下 所有子 录*

```
Files.walkFileTree(Path.of("/*), new SiapleFileVisitor<Path>()
   {
      public FileVisitResult preVisitDirectory(Path path, BasicFileAttributes attrs)
            throws IOException
      {
         System.out.printin(path);
         return FileVisitResult.CONTINUE;
      }
      public FileVisitResult postVisitDirectory(Path dir, IOException e)
      {
         return FileVisitResult.CONTINUE;
      }
      public FileVisitResult visitFileFailed(Path path, IOException e) throws IOException
      {
         return FileVisitResult.SKIP SUBTREE;
      }
   })
```

*值得注意 是 我们 postVisitDirectory方法和visitFileFailed方法 否则 会在 到不允 打开 录或不允 文件时 即失 。*

*应 注意 是 径 众多属性是作为preVisitDirectory和visitFile方法 参数传 。 不得不 操作 来 得 些属性 因为它 区分文件和 录。因 此 你就不 再次执 了。*

*如果你 在 入或 开一个 录时执 某些操作 么FileVisitor接口 其他方法就 显得 常有 了。例如 在删 录树时 在 当前 录 所有文件之后 才 该目录。下 是删 录树 完整代*

```
// Delete the directory tree starting at root
Files.walkFileTree(root, new SimpleFileVisitor<Path>()
   {
      public FileVisitResult visitFile(Path file, BasicFileAttributes attrs)
            throws IOException
      {
         Files.delete(file);
         return FileVisitResult.CONTINUE;
      }
      public FileVisitResult postVisitDirectory(Path dir, IOException e) throws IOException
```

```
if (e != null) throw e;
Files.delete(dir);
return FileVisitResult.CONTINUE;
}
});
```

#### API java.nio.file.Files

- static DirectoryStream<Path> newDirectoryStream(Path path)
- static DirectoryStream
   Path> newDirectoryStream(Path path, String glob)
   获取给定目录中可以遍历所有文件和目录的迭代器。第二个方法只接受那些与给定的glob 模式匹配的项。
- static Path walkFileTree(Path start, FileVisitor<? super Path> visitor) 遍历给定路径的所有子孙,并将访问器应用于这些子孙之上。

#### API java.nio.file.SimpleFileVisitor<T>

- static FileVisitResult visitFile(T path, BasicFileAttributes attrs)
   在访问文件或目录时被调用,返回 CONTINUE、SKIP\_SUBTREE、SKIP\_SIBLINGS 和 TERMINATE
   之一,默认实现是不做任何操作而继续访问。
- static FileVisitResult preVisitDirectory(T dir, BasicFileAttributes attrs)
- static FileVisitResult postVisitDirectory(T dir, BasicFileAttributes attrs)
   在访问目录之前和之后被调用,默认实现是不做任何操作而继续访问。
- static FileVisitResult visitFileFailed(T path, I0Exception exc)
   如果在试图获取给定文件的信息时抛出异常,则该方法被调用。默认实现是重新抛出异常,这会导致访问操作以这个异常而终止。如果你想继续访问,则需要覆盖这个方法。

#### 2.4.8 ZIP 文件系统

Paths 类会在默认文件系统中查找路径,即在用户本地磁盘中的文件。你也可以有别的文件系统,其中最有用的之一是 ZIP 文件系统。如果 zipname 是某个 ZIP 文件的名字,那么下面的调用

FileSystem fs = FileSystems.newFileSystem(Path.of(zipname));

将建立一个文件系统,它包含 ZIP 文档中的所有文件。如果知道文件名,那么从 ZIP 文档中复制出这个文件就会变得很容易:

Files.copy(fs.getPath(sourceName), targetPath);

其中的 fs.getPath 对于任意文件系统来说都与 Paths.get 类似。

要列出 ZIP 文档中的所有文件,可以遍历文件树:

```
FileSystem fs = FileSystems.newFileSystem(Path.of(zipname));
Files.walkFileTree(fs.getPath("/"), new SimpleFileVisitor<Path>()
```

```
throws IOException
   {
      System.out printin(file);
      return FileVisitResult.CONTINUE;
   }
})
```

*比2.2.3 中描述的API 好 后 使 是多个专 处 ZIP文档 新 。*

# *叫 java.nio.file.FileSysteas*

*• static FileSystem newFileSystem(Path path) 回 一个可以接受 定 径 文件 提供 创建 文件 。 汄情况下 对 于ZIP文件 是有一个提供 它接受名字以.zip或.jar <sup>尾</sup> 文件。*

# *\_ java.nio.file.FileSyste\**

*• static Path getPath(String first, String.., more) 将 定 字 串 接 来创建一个 径。*

# *2.5内存映射文件*

*大多数操作 可以利 拟内存实 来将一个文件或 文件 一 分"映射"到内 存中。然后 个文件就可以 当作内存数 一样地 比传 文件操作 快得多。*

# *2.5.1内存映射文件 <sup>性</sup>*

*在本 末尾 你可以 到一个 传 文件 入和内存映射文件 CRC32校 和 <sup>序</sup>。在同一台机器上 我们对JDK j <sup>e</sup><sup>八</sup>ib 录中49MB src.zip文件 不同 <sup>方</sup> 式来 校 和 录下来 时 数据如 2-6所 。*

| 方法           | 时   |
|--------------|-----|
| 普通输入流        | 110 |
| 带<br>冲<br>入流 | 9.9 |
| 机<br>文件      | 102 |
| 内存映射文件       | 7.2 |

*2-6文件操作 <sup>处</sup> <sup>时</sup> 数据*

*正如你所 在 台 定 机器上 内存映射比使 带 冲 序 人 微快一点, 但是比使 RandomAccessFile快很多。*

*当然 值因机器不同会产 很大 差异 但是很明显 与 机 比 性 提 总是很显著的。另一方 对于中 尺寸文件 序 人则没有必 使 内存映射。*

*java.nio包使内存映射变得十分 单 下 就是我们需要做 。*

首先,从文件中获得一个通道(channel),通道是用于磁盘文件的一种抽象,它使我们可以访问诸如内存映射、文件加锁机制以及文件间快速数据传递等操作系统特性。

FileChannel channel = FileChannel.open(path, options);

然后,通过调用 FileChannel 类的 map 方法从这个通道中获得一个 ByteBuffer。你可以指定想要映射的文件区域与映射模式,支持的模式有三种:

- FileChannel.MapMode.READ\_ONLY: 所产生的缓冲区是只读的,任何对该缓冲区写人的尝试都会导致 ReadOnlyBufferException 异常。
- FileChannel.MapMode.READ\_WRITE: 所产生的缓冲区是可写的,任何修改都会在某个时刻写回到文件中。注意,其他映射同一个文件的程序可能不能立即看到这些修改,多个程序同时进行文件映射的确切行为是依赖于操作系统的。
- FileChannel.MapMode.PRIVATE: 所产生的缓冲区是可写的,但是任何修改对这个缓冲区来说都是私有的,不会传播到文件中。

例如,

MappedByteBuffer buffer = channel.map(FileChannel.MapMode.READ\_ONLY, 0, channel.size());

一旦有了缓冲区,就可以使用 ByteBuffer 类和 Buffer 超类的方法读写数据了。

缓冲区支持顺序和随机数据访问,它有一个可以通过 get 和 put 操作来移动的位置。例如,可以像下面这样顺序遍历缓冲区中的所有字节:

```
while (buffer.hasRemaining())
{
   byte b = buffer.get();
   . . .
}
```

或者, 像下面这样进行随机访问:

```
for (int i = 0; i < buffer.limit(); i++)
{
   byte b = buffer.get(i);
   . . .
}</pre>
```

你可以用下面的方法来读写字节数组:

```
get(byte[] bytes)
get(byte[] bytes, int offset, int length)
```

最后,还有下面的方法:

```
getInt getChar
getLong getFloat
getShort getDouble
```

用来读入在文件中存储为二进制值的基本类型值。正如我们提到的, Java 对二进制数据使用高位在前的排序机制, 但是, 如果需要以低位在前的排序方式处理包含二进制数字的文件, 那么只需调用

buffer.order(ByteOrder.LITTLE\_ENDIAN);

要查询缓冲区内当前的字节顺序, 可以调用:

ByteOrder b = buffer.order();

要向缓冲区写数字,可以使用下列的方法:

putInt putChar putFloat putShort putDouble

在恰当的时机, 以及当通道关闭时, 会将这些修改写回到文件中。

程序清单 2-5 用于计算文件的 32 位的循环冗余校验和(CRC32),这个数值就是经常用来判断一个文件是否已损坏的校验和,因为文件损坏极有可能导致校验和改变。java.util.zip 包中包含一个 CRC32 类,可以使用下面的循环来计算一个字节序列的校验和:

```
var crc = new CRC32();
while (more bytes)
    crc.update(next byte);
long checksum = crc.getValue();
```

CRC 计算的细节并不重要,我们只是将它作为一个有用的文件操作的实例来使用。(在实践中,每次会以更大的块而不是一个字节为单位来读取和更新数据,而它们的速度差异并不明显。) 应该像下面这样运行程序:

java memoryMap.MemoryMapTest filename

#### 程序清单 2-5 memoryMap/MemoryMapTest.java

```
package memoryMap;
3 import java.io.*;
4 import java.nio.*;
5 import java.nio.channels.*;
6 import java.nio.file.*;
7 import java.util.zip.*;
8
9
   * This program computes the CRC checksum of a file in four ways. <br>
   * Usage: java memoryMap.MemoryMapTest filename
12
    * @version 1.03 2018-05-01
   * @author Cay Horstmann
13
14
15 public class MemoryMapTest
16 {
      public static long checksumInputStream(Path filename) throws IOException
17
18
         try (InputStream in = Files.newInputStream(filename))
19
28
            var crc = new CRC32():
21
            boolean done = false:
22
            while (!done)
23
24
               int c = in.read();
25
```

```
if (c == -1) done = true;
26
                else crc.update(c);
27
28
            return crc.getValue();
29
         }
38
      }
31
32
      public static long checksumBufferedInputStream(Path filename) throws IOException
33
34
         try (var in = new BufferedInputStream(Files.newInputStream(filename)))
35
36
            var crc = new CRC32();
37
38
            boolean done = false;
39
            while (!done)
48
            {
41
                int c = in.read();
42
                if (c == -1) done = true;
43
                else crc.update(c);
44
45
            return crc.getValue();
46
47
      }
48
49
58
      public static long checksumRandomAccessFile(Path filename) throws IOException
51
          try (var file = new RandomAccessFile(filename.toFile(), "r"))
52
53
             long length = file.length();
54
             var crc = new CRC32();
55
56
             for (long p = 0; p < length; p++)
57
58
             {
                int c = file.readByte();
59
                crc.update(c);
69
             }
61
62
             return crc.getValue();
63
      }
64
65
      public static long checksumMappedFile(Path filename) throws IOException
66
67
          try (FileChannel channel = FileChannel.open(filename))
68
69
70
             var crc = new CRC32();
             int length = (int) channel.size();
71
             MappedByteBuffer buffer = channel.map(FileChannel.MapMode.READ ONLY, 0, length);
72
73
             for (int p = 0; p < length; p++)
74
75
             {
                int c = buffer.get(p);
76
                crc.update(c);
77
78
             return crc.getValue();
79
RA
```

```
81
82
      public static void main(String[] args) throws IOException
83
84
         System.out.println("Input Stream:");
85
         long start = System.currentTimeMillis();
26
         Path filename = Path.of(args[0]):
87
         long crcValue = checksumInputStream(filename);
88
         long end = System.currentTimeMillis();
RQ
         System.out.println(Long.toHexString(crcValue));
         System.out.println((end - start) + " milliseconds");
91
97
         System.out.println("Buffered Input Stream:");
93
         start = System.currentTimeMillis();
94
95
         crcValue = checksumBufferedInputStream(filename);
         end = System.currentTimeMillis();
96
         System.out.println(Long.toHexString(crcValue));
97
         System.out.println((end - start) + " milliseconds");
98
99
         System.out.println("Random Access File:");
188
101
          start = System.currentTimeMillis();
          crcValue = checksumRandomAccessFile(filename);
182
          end = System.currentTimeMillis():
103
         System.out.println(Long.toHexString(crcValue));
194
         System.out.println((end - start) + " milliseconds");
105
196
          System.out.println("Mapped File:");
107
          start = System.currentTimeMillis();
188
          crcValue = checksumMappedFile(filename);
189
          end = System.currentTimeMillis();
110
          System.out.println(Long.toHexString(crcValue));
111
112
          System.out.println((end - start) + " milliseconds");
113
114 }
```

# API java.io.FileInputStream

FileChannel getChannel() 1.4
 返回用于访问这个输入流的通道。

# API java.io.FileOutputStream

FileChannel getChannel() 1.4
 返回用于访问这个输出流的通道。

# API java.io.RandomAccessFile

FileChannel getChannel() 1.4
 返回用于访问这个文件的通道。

# para.nio.channels.FileChannel

• static FileChannel open(Path path, OpenOption... options) 7

打开指定路径的文件通道,默认情况下,通道打开时用于读入。参数 options 是 Standard-OpenOption 枚举中的 WRITE、APPEND、TRUNCATE EXISTING、CREATE 值。

■ MappedByteBuffer map(FileChannel.MapMode mode, long position, long size)
 将文件的一个区域映射到内存中。参数 mode 是 FileChannel.MapMode 类中的常量 READ\_ONLY、READ WRITE 或 PRIVATE 之一。

#### API java.nio.Buffer 1.4

- boolean hasRemaining()
   如果当前的缓冲区位置没有到达这个缓冲区的界限位置,则返回 true。
- int limit() 返回这个缓冲区的界限位置,即没有任何值可用的第一个位置。

### API java.nio.ByteBuffer

- byte get()从当前位置获得一个字节,并将当前位置移动到下一个字节。
- byte get(int index)从指定索引处获得一个字节。
- ByteBuffer put(byte b)
   向当前位置推入一个字节,并将当前位置移动到下一个字节。返回对这个缓冲区的引用。
- ByteBuffer put(int index, byte b)
   向指定索引处推入一个字节。返回对这个缓冲区的引用。
- ByteBuffer get(byte[] destination)
- ByteBuffer get(byte[] destination, int offset, int length)
   用缓冲区中的字节来填充字节数组,或者字节数组的某个区域,并将当前位置向前移动读入的字节数个位置。如果缓冲区不够大,那么就不会读入任何字节,并抛出BufferUnderflowException。返回对这个缓冲区的引用。
- ByteBuffer put(byte[] source)
- ByteBuffer put(byte[] source, int offset, int length)
   将字节数组中的所有字节或者给定区域的字节都推入缓冲区中,并将当前位置向前移动写出的字节数个位置。如果缓冲区不够大,那么就不会读入任何字节,并抛出BufferUnderflowException。返回对这个缓冲区的引用。
- Xxx getXxx()
- Xxx getXxx(int index)
- ByteBuffer putXxx(Xxx value)
- ByteBuffer putXxx(int index, Xxx value)
   获得或放置一个二进制数。Xxx 是 Int、Long、Short、Char、Float 或 Double 中的一个。

- ByteBuffer order(ByteOrder order)
- ByteOrder order()
   设置或获得字节顺序, order 的值是 ByteOrder 类的常量 BIG\_ENDIAN 或 LITTLE\_ENDIAN 中的一个。
- static ByteBuffer allocate(int capacity)
   构建具有给定容量的缓冲区。
- static ByteBuffer wrap(byte[] values)
   构建具有指定容量的缓冲区,该缓冲区是对给定数组的包装。
- CharBuffer asCharBuffer()
   构建字符缓冲区,它是对这个缓冲区的包装。对该字符缓冲区的变更将在这个缓冲区中反映出来,但是该字符缓冲区有自己的位置、界限和标记。

#### API java.nio.CharBuffer

- char get()
- CharBuffer get(char[] destination)
- CharBuffer get(char[] destination, int offset, int length)
   从这个缓冲区的当前位置开始,获取一个 char 值,或者一个范围内的所有 char 值,然后将位置向前移动以越过所有读入的字符。最后两个方法将返回 this。
- CharBuffer put(char c)
- CharBuffer put(char[] source)
- CharBuffer put(char[] source, int offset, int length)
- CharBuffer put(String source)
- CharBuffer put (CharBuffer source)
   从这个缓冲区的当前位置开始,放置一个 char 值,或者一个范围内的所有 char 值,然后将位置向前移动越过所有被写出的字符。当放置的值是从 CharBuffer 读入时,将读入所有剩余字符。所有方法将返回 this。

# 2.5.2 缓冲区数据结构

在使用内存映射时,我们创建了单一的缓冲区横跨整个文件或我们感兴趣的文件区域。 我们还可以使用更多的缓冲区来读写大小适度的信息块。

本节将简要地介绍 Buffer 对象上的基本操作。缓冲区是由具有相同类型的数值构成的数组,Buffer 类是一个抽象类,它有众多的具体子类,包括 ByteBuffer、CharBuffer、DoubleBuffer、IntBuffer、LongBuffer和 ShortBuffer。

# i 注释: StringBuffer 类与这些缓冲区没有关系。

在实践中,最常用的将是 ByteBuffer 和 CharBuffer。如图 2-9 所示,每个缓冲区都具有:

- *一个容 它永 不 改变。*
- *一个 写位 下一个值将在此 写。*
- *一个 它 写是没有意义 。*
- *一个可 标 于 复一个 人或写出操作。*

*些值满 下面的条件*

#### *0 标 写位 界限名容*

![](_page_122_Figure_8.jpeg)

*使 冲区 主 是执 "写 然后 人"循 。假 我们有一个 冲区 在一开 <sup>始</sup> <sup>它</sup> <sup>位</sup> <sup>为</sup>0, 于容 。我们不断地 put将值添加到 <sup>个</sup> 冲区中 当我们 尽所有 数据或 写出 数据量达到容 大小时 就 切换到 入操作了。*

*<sup>时</sup> flip方法将 到当前位 并把位 复位到0。 在在remaining方法 回正数时(它 回 值是 -位 ) 不断地调用get。在我们将 冲区中所有 值 人之后 调用clear<sup>使</sup> 冲区为下一次写循 做好准备。clear方法将位 复位到0,并将 复位到容 。*

*如果你想 冲区 可以使 rewind或mark/reset方法 内容 査 API注 。 取 冲区 可以调用诸如ByteBuffer.allocate或ByteBuffer.wrap 样 态方法。 然后 可以 来 某个 数据填充 冲区 或 将 冲区 内容写出到 中。例如*

*ByteBuffer buffer <sup>=</sup> ByteBuffer.allocate(RECORD SIZE); channel.read(buffer); channel.position(newpos); buffer.flipO; channel.write(buffer);*

*是一 常有 方法 可以替代 机 文件。*

# *^ijava.nio.Buffer*

*• Buffer clear()*

*将位 复位到o,并将界限设置到容 <sup>使</sup> <sup>个</sup> 冲区为写出做好准备。 <sup>回</sup>this。*

- Buffer flip()
  - 通过将界限设置到位置,并将位置复位到 0,使这个缓冲区为读入做好准备。返回 this。
- Buffer rewind()

通过将读写位置复位到 0, 并保持界限不变, 使这个缓冲区为重新读人相同的值做好准备。返回 this。

• Buffer mark()

将这个缓冲区的标记设置到读写位置,返回 this。

• Buffer reset()

将这个缓冲区的位置设置到标记,从而允许被标记的部分再次被读入或写出,返回 this。

int remaining()

返回剩余可读入或可写出的值的数量,即界限与位置之间的差异。

- int position()
- void position(int newValue)返回这个缓冲区的位置。
- int capacity()返回这个缓冲区的容量。

# 2.6 文件加锁机制

考虑一下多个同时执行的程序需要修改同一个文件的情形,很明显,这些程序需要以某种方式进行通信,不然这个文件很容易被损坏。文件锁可以解决这个问题,它可以控制对文件或文件中某个范围的字节的访问。

假设你的应用程序将用户的偏好存储在一个配置文件中,当用户调用这个应用的两个实例时,这两个实例就有可能会同时希望写配置文件。在这种情况下,第一个实例应该锁定文件,当第二个实例发现文件被锁定时,它必须决策是等待直至文件解锁,还是直接跳过这个写操作过程。

要锁定一个文件,可以调用 FileChannel 类的 lock 或 tryLock 方法:

FileChannel = FileChannel.open(path);
FileLock lock = channel.lock();

或

FileLock lock = channel.tryLock();

第一个调用会阻塞直至可获得锁,而第二个调用将立即返回,要么返回锁,要么在锁不可获得的情况下返回 null。这个文件将保持锁定状态,直至通道关闭,或者在锁上调用了 release 方法。

你还可以通过下面的调用锁定文件的一部分:

FileLock lock(long start, long size, boolean shared)

或

FileLock tryLock(long start, long size, boolean shared)

如果 shared 标志为 false,则锁定文件的目的是读写;而如果为 true,则这是一个共享锁,允许多个进程从文件中读入,并阻止任何进程获得独占的锁。并非所有的操作系统都支持共享锁,因此你可能会在请求共享锁的时候得到独占的锁。调用 FileLock 类的 isShared 方法可以查询所持有的锁的类型。

這一注释:如果你锁定了文件的尾部,而这个文件的长度随后增长并超过了锁定的部分,那么增长出来的额外区域是未锁定的,要想锁定所有的字节,可以使用 Long.MAX\_VALUE 来表示尺寸。

要确保在操作完成时释放锁,与往常一样,最好在一个带资源的 try 语句中执行释放锁的操作:

```
try (FileLock lock = channel.lock())
{
   access the locked file or segment
}
```

请记住,文件加锁机制是依赖于操作系统的,下面是需要注意的几点:

- 在某些系统中,文件加锁仅仅是建议性的,如果一个应用未能得到锁,它仍旧可以向被另一个应用并发锁定的文件执行写操作。
- 在某些系统中,不能在锁定一个文件的同时将其映射到内存中。
- 文件锁是由整个 Java 虚拟机持有的。在同一个虚拟机上执行的并发任务不可能每一个都获得一个在同一个文件上的锁。当调用 lock 和 tryLock 方法时,如果虚拟机已经在同一个文件上持有了另一个重叠的锁,那么这两个方法将抛出 OverlappingFileLockException。
- 在一些系统中,关闭一个通道会释放由 Java 虚拟机持有的底层文件上的所有锁。因此,在同一个锁定文件上应避免使用多个通道。
- 在网络文件系统上锁定文件是高度依赖于系统的, 因此应该尽量避免。

# API java.nio.channels.FileChannel

- FileLock lock()在整个文件上获得一个独占的锁,这个方法将阻塞直至获得锁。
- FileLock tryLock()在整个文件上获得一个独占的锁,或者在无法获得锁的情况下返回 null。
- FileLock lock(long position, long size, boolean shared)
- FileLock tryLock(long position, long size, boolean shared)
   在文件的一个区域上获得锁。第一个方法将阻塞直至获得锁,而第二个方法将在无法

获得锁时返回 null。参数 shared 的值为 true 表示共享锁,为 false 表示独占锁。

#### API java.nio.channels.FileLock

void close() 1.7 释放这个锁。

# 2.7 正则表达式

正则表达式 (regular expression) 用于指定字符串的模式,可以在任何需要定位匹配某种特定模式的字符串的情况下使用正则表达式。例如,我们有一个示例程序就是用来定位HTML 文件中的所有超链接的,它是通过查找 <a href = "...">模式的字符串来实现此目的的。

当然,在指定模式时,...标记法并不够精确。需要精确地指定什么样的字符序列才是合法的匹配,这就要求无论何时,当你要描述一个模式时,都需要使用某种特定的语法。

在下面各节中,我们将介绍 Java API 用到的正则表达式的语法,并讨论如何使用正则表达式。

#### 2.7.1 正则表达式语法

下面是一个简单的示例, 正则表达式

[Jj]ava.+

匹配下列形式的所有字符串:

- 第一个字母是 J 或 j。
- 接下来的三个字母是 ava。
- 字符串的其余部分由一个或多个任意的字符构成。

例如,字符串 "javanese" 就匹配这个特定的正则表达式,但是字符串 "Core Java" 就不匹配。 正如你所见,你需要了解一点这种语法,以理解正则表达式的含义。幸运的是,对于大 多数情况,一小部分很直观的语法结构就足够用了。

在正则表达式中,字符表示其自身,除非它是下列保留字符之一:

. \* + ? { | ( ) [ \ ^ \$

例如,正则表达式 Java 只能匹配字符串 Java。

符号,可以匹配任意单个字符。例如, .a.a 可以匹配 Java 和 data。

符号\*表示其之前的结构可以重复0或多次,而符号+表示1或多次。后缀?表示某个结构是可选的(0或1次)。例如,be+s?可以匹配 be、bee 和 bees。你可以用 {} 指定其他类型的出现次数,请查看表 2-7。

符号 | 表示选择, .(oo|ee)f 可以匹配 beef 或 woof。注意, 如果没有括号, .oo|eef 就变成了在 .oo 和 eef 之间选择。括号还可以用于群组,请查看 2.7.4 节。

字符类 (character class) 是一个括在括号中的可选择的字符集, 例如 [Jj]、[0-9]、

[A-Za-z] 或 [^0-9]。在字符类内部, -表示一个范围(所有 Unicode 值落在两个边界范围之内的字符),但是,如果 -是字符类中的第一个或最后一个字符,那么它表示的是其自身。如果 ^是字符类中的第一个字符,则表示补集(除了指定字符之外的所有字符)。

有许多预定义的字符类 (predefined character class), 例如 \d (数字) 和 \p{Sc} (Unicode 货币符号)。请查看表 2-7 和表 2-8。

字符 ^ 和 \$ 匹配的是输入的开头和结尾。

如果你需要的是字面意思的 .\*+?{|()[\^\$,则需要在前面加一个反斜杠。在字符类内部,你只需要转译 [和\,前提是仔细处理]-^的位置。例如,[]^-]就包含了这三个字符的类。

或者, 你可以用 \Q 和 \E 把字符串括起来。例如, \(\\$0\.99\) 和 \Q(\$0.99)\E 都可以匹配字符串(\$0.99)。

√ 提示: 如果字符串包含正则表达式语法中众多特殊字符的某些字符,那么你可以通过调用 Parse.quote(str)对它们进行转义。这样做会直接用 \Q 和 \E 把这个字符串括起来,而且可以处理好 str 中包含 \E 的特殊情况。

| キッフ   | 元明中华于海  | + |
|-------|---------|---|
| 表 2-7 | 正则表达式语法 | 厷 |

| 表达式                                             | 描述                                                                 | 示 例                                                         |
|-------------------------------------------------|--------------------------------------------------------------------|-------------------------------------------------------------|
| 字符                                              |                                                                    |                                                             |
| c,除.*+?{ ()[\^\$之外                              | 字符 c                                                               | J                                                           |
|                                                 | 任何除行终止符之外的字符,或者在<br>DOTALL 标志被设置时表示任何字符                            |                                                             |
| \X{p}                                           | 十六进制码为 p 的 Unicode 码点                                              | \x{1D546}                                                   |
| \uhhhh,\xhh,\0o,\0oo,\0oo                       | 具有给定十六进制或八进制值的码元                                                   | \uFEFF                                                      |
| \a,\e,\f,\n,\r,\t                               | 响铃符(\x{7})、转义符(\x{1B})、换页符(\x{8})、换行符(\x{A})、回车符(\x{D})、指标符(\x{9}) | \n                                                          |
| \cc, 其中c在[A-Z]的范围内,或者是@[\]^_?之一                 | 对应于字符 c 的控制字符                                                      | \cH 是退格符 (\x{8})                                            |
| \c, 其中 c 不在 [A-Za-z0-9] 的<br>范围内                | 字符 c                                                               | \\                                                          |
| \Q\E                                            | 在左引号和右引号之间的所有字符                                                    | \Q()\E 匹配字符串 ()                                             |
| 字符类                                             |                                                                    |                                                             |
| $[C_1C_2]$ , 其中 $C_i$ 是多个字符, 范围从 $c-d$ , 或者是字符类 | 任何由 $C_1$ , $C_2$ , …表示的字符                                         | [0-9+-]                                                     |
| [^]                                             | 某个字符类的补集                                                           | [^\d\s]                                                     |
| [&&]                                            | 字符集的交集                                                             | [\p{L}&&[^A-Za-z]]                                          |
| ,                                               | 某个预定义字符类(参阅表 2-8);它的补集                                             | \p{L} 匹配一个 Unicode 字母, 而 \pL<br>也匹配这个字母, 可以忽略单个字<br>母情况下的括号 |
| \d, \D                                          | 数字([θ-9], 或者在 UNICODE_CHARACTER_CLASS 标志被设置时表示 \p{Digit}); 它的补集    | \d+ 是一个数字序列                                                 |

(续)

| 表达式                                                                        | 描述                                                                                  | 示 例                                              |  |
|----------------------------------------------------------------------------|-------------------------------------------------------------------------------------|--------------------------------------------------|--|
| \w, \W                                                                     | 单词字符([a-zA-Z0-9], 或者在 UNICODE_CH-ARACTER_CLASS 标志被设置时表示 Unicode 单词字符);它的补集          |                                                  |  |
| \s, \S                                                                     | 空格([\n\r\t\f\x{B}],或者在UNICODE_CHA-<br>RACTER_CLASS 标志被设置时表示IsWhite_<br>Space});它的补集 | \s*,\s*是由可选的空格字符包围的逗号                            |  |
| \h, \v, \H, \V                                                             | 水平空白字符、垂直空白字符,它们的<br>补集                                                             |                                                  |  |
| 序列和选择                                                                      |                                                                                     |                                                  |  |
| XY                                                                         | 任何 X 中的字符串,后面跟随任何 Y 中的字符串                                                           | [1-9][0-9]*表示没有前导零的正整数                           |  |
| X Y                                                                        | 任何X或Y中的字符串                                                                          | httplftp                                         |  |
| 群组                                                                         |                                                                                     |                                                  |  |
| (X)                                                                        | 捕获X的匹配                                                                              | ''([^']*)' 捕获的是被引用的文本                            |  |
| \n                                                                         | 第n组                                                                                 | (['"]).*\1可以匹配 'Fred' 和 "Fred",<br>但是不能匹配 "Fred' |  |
| (? <name>X)</name>                                                         | 捕获与给定名字匹配的 X                                                                        | '(7 <id>[A-Za-z0-9]+)' 可以捕获名字<br/>为 id 的匹配</id>  |  |
| \k <name></name>                                                           | 具有给定名字的组                                                                            | \k <id>可以匹配名字为 id 的组</id>                        |  |
| (?:X)                                                                      | 使用括号但是不捕获 X                                                                         | 在 (?:http ftp)://(.*) 中, 在://之<br>后的匹配是 \1       |  |
| (?f,f <sub>2</sub> :X)<br>(?f,f <sub>k</sub> :X), 其中f,在 [dimsultx]<br>的范围中 | 匹配但是不捕获给定标志开或关(在 - 之后)的 X                                                           | (?i:jpe?g) 是大小写不敏感的匹配                            |  |
| 其他 (?)                                                                     | 请参阅 Pattern API 文档                                                                  |                                                  |  |
| 量词                                                                         |                                                                                     |                                                  |  |
| X?                                                                         | 可选X                                                                                 | \+? 是可选的 + 号                                     |  |
| X*, X+                                                                     | 0 或多个 X, 1 或多个 X                                                                    | [1-9][0-9]+是大于等于 10 的整数                          |  |
| $X\{n\}$ , $X\{n,\}$ , $X\{m,n\}$                                          | $n \uparrow X$ , 至少 $n \uparrow X$ , $m $ 到 $n \uparrow X$                          | [0-7]{1,3} 是一位到三位的八进制数                           |  |
| Q?,其中 $Q$ 是一个量词表达式                                                         | 勉强量词,在尝试最长匹配之前先尝试<br>最短匹配                                                           | .*(<.+?>).* 捕获尖括号括起来的最短序列                        |  |
| Q+, 其中 Q 是一个量词表达式                                                          | 占有量词,在不回溯的情况下获取最长 匹配                                                                | '[^']*+' 匹配单引号引起来的字符串,并且在字符串中没有右单引号的情况下立即匹配失败    |  |
| 边界匹配                                                                       |                                                                                     |                                                  |  |
| ^, \$                                                                      | 输入的开头和结尾(或者多行模式中的开<br>头和结尾行)                                                        | ^Java\$ 匹配输入中的 Java 或 Java 构成的行                  |  |
| \A, \Z, \z                                                                 | 输入的开头、输入的结尾、输入的绝对<br>结尾(在多行模式中不会发生变化)                                               |                                                  |  |
| \b, \B                                                                     | 单词边界, 非单词边界                                                                         | \bJava\b 匹配单词 Java                               |  |
| \R                                                                         | Unicode 行分隔符                                                                        |                                                  |  |
| \G                                                                         | 前一个匹配的结尾                                                                            |                                                  |  |

| 字符类名字 解释                                                     |                                                                                                                                                                         |  |
|--------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|
| posixClass                                                   | posixClass 是 Lower、Upper、Alpha、Digit、Alnum、Punct、Graph、Print、Cntrl、XDigit、Space、Blank、ASCII 之一,它会依 UNICODE_CHARACTER_CLASS 标志的值而被解释为 POSIX 或 Unicode 类                  |  |
| IsScript,sc=Script,<br>script=Script                         | Character.UnicodeScript.forName 可以接受的脚本                                                                                                                                 |  |
| InBlock, blk=Block, block=Block                              | Character.UnicodeScript.forName 可以接受的块                                                                                                                                  |  |
| Category, InCategory, gc=Category, general_category=Category | Unicode 通用分类的单字母或双字母名字                                                                                                                                                  |  |
| Is <i>Property</i>                                           | Property 是 Alphabetic、Ideographic、Letter、Lowercase、Uppercase、Titlecase、Punctuation、Control、White Space、Digit、Hex Digit、Join Control、Noncharacter Code Point、Assigned 之一 |  |
| java <i>Method</i>                                           | 调用 Character.is Method 方法 (必须不是过时的方法)                                                                                                                                   |  |

表 2-8 与 \p 一起使用的预定义字符类名字

遗憾的是,在使用正则表达式的各种程序和类库之间,表达式语法并未完全标准化。尽管在基本结构上达成了一致,但是它们在细节上仍旧存在着许多令人抓狂的差异。Java 正则表达式类使用的语法与 Perl 语言使用的语法十分相似,但是并不完全一样。表 2-7 展示的是 Java 语法中的所有结构。关于正则表达式语法的更多信息,可以求教于 Pattern 类的 API 文档和 Jeffrey E. F. Friedl 的 *Mastering Regular Expressions* (O' Reilly and Associates, 2006)。

#### 2.7.2 匹配整个字符串

通常,使用正则表达式的方式有两种:检测某个字符串是否与正则表达式匹配,或者查找出字符串中所有与正则表达式匹配的部分。

第一种情况可以直接使用 matches 方法:

```
String regex = "-]?\\d+";
CharSequence input = . . .;\nif (Pattern.matches(regex, input))
{
    . . .
}
```

如果需要多次使用同一个正则表达式,那么更高效的方式是编译它,然后为每一个输入都创建一个Matcher:

```
Pattern pattern = Pattern.compile(regex);
Matcher matcher = pattern.matcher(input);\nif (matcher.matches()) . . .
```

如果匹配成功,那么可以获取匹配群组的位置,详情请查看下一节。如果想要匹配集合或流中的元素,则可以将模式转换为谓词:

```
Stream<String> strings = . . .;
List<String> result = strings.filter(pattern.asPredicate()).toList();
```

其结果将包含所有满足条件的字符串,即它们都包含正则表达式的匹配。

若要匹配整个字符串,则可以改用 pattern.asMatchPredicate()。

#### 2.7.3 找出字符串中的所有匹配

本节将讨论正则表达式的另一种常见用法——在输入中查找所有匹配。此时,可以使用下面的循环:

```
String input = . . .;
Matcher matcher = pattern.matcher(input);
while (matcher.find())
{
    String match = matcher.group();
    int matchStart = matcher.start();
    int matchEnd = matcher.end();
    . . .
}
```

在这种方式中,可以依次处理每个匹配。正如上面的代码片段所示,可以获取匹配的字符串,以及它在输入字符串中的位置。

更优雅的是,可以调用 results 方法来获取一个 Stream≺MatchResult>。MatchResult 接口有group、start 和 end 方法,就像 Matcher 一样。(事实上,Matcher 类实现了这个接口。)下面展示了如何获取所有匹配的列表:

```
List<String> matches = pattern.matcher(input)
   .results()
   .map(Matcher::group)
   .toList();
```

如果要处理的是文件中的数据,那么可以使用 Scanner.findAll 方法来获取一个 Stream<Match-Result>,这样就无须先将内容读取到一个字符串中。可以给 Scanner 传递一个 Pattern 或一个模式字符串:

```
Scanner in = new Scanner(path, "UTF_8");
Stream<String> words = in.findAll("\\pL+")
    .map(MatchResult::group);
```

程序清单 2-6 对这种机制进行了应用,它定位一个 Web 页面上的所有超文本引用,并打印它们。为了运行这个程序,需要在命令行中提供一个 URL,例如:

java match.HrefMatch http://horstmann.com

#### 程序清单 2-6 match/HrefMatch.java

```
package match;
\nimport java.io.*;\nimport java.net.*;\nimport java.nio.charset.*;\nimport java.util.regex.*;

* This program displays all URLs in a web page by matching a regular expression that
tell * describes the <a href=...> HTML tag. Start the program as <br/>
* This program of the start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <br/>
* describes the <a href=...> HTML tag. Start the program as <a href=...> HTML tag. Start the program as <a href=...> HTML tag. Start the program as <a href=...> HTML tag. Start the program as <a href=...> HTML t
```

```
* java match.HrefMatch URL
11
12
    * @version 1.04 2019-08-28
    * @author Cay Horstmann
13
14
   public class HrefMatch
15
16
      public static void main(String[] args)
17
18
         try
19
28
         {
            // get URL string from command line or use default
21
            String urlString;
22
            if (args.length > 0) urlString = args[0];
23
            else urlString = "http://openjdk.java.net/";
24
25
            // read contents of URL
26
            InputStream in = new URL(urlString).openStream();
27
            var input = new String(in.readAllBytes(), StandardCharsets.UTF 8);
28
29
            // search for all occurrences of pattern
38
            String patternString = "<a\\s+href\\s*=\\s*(\"[^\\"]*\"|[^\\s>]*)\\s*>";
31
            Pattern pattern = Pattern.compile(patternString, Pattern.CASE INSENSITIVE);
32
            pattern.matcher(input)
33
                .results()
34
35
                .map(MatchResult::group)
                .forEach(System.out::println);
36
37
         catch (IOException | PatternSyntaxException e)
38
39
            e.printStackTrace();
48
41
42
   }
43
```

#### 2.7.4 群组

用群组来抽取匹配中的各个组成部分是一种常见操作。例如,假设在发票上有一行,包含产品名称、数量和单位价格,就像下面这样:

Blackwell Toaster USD29.95

下面的正则表达式包含针对这一行中每一个组成部分的群组:

 $(p{Alnum}+(s+p{Alnum}+)*)(A-Z]{3})([0-9.]*)$ 

在匹配后, 我们可以像下面这样从匹配器中抽取第 n 个群组:

String contents = matcher.group(n);

群组是按照左括号排序的,编号从1开始(群组0是整个输入)。在上面的例子中,我们可以像下面这样将输入断开:

```
Matcher matcher = pattern.matcher(input);\nif (matcher.matches())
{
```

```
item = matcher.group(1);
currency = matcher.group(3);
price = matcher.group(4);
```

我们对群组2并不感兴趣,因为它只是由表示产品名称可能存在重复内容的括号所产生的群组。为了将意图表示得更清楚,可以使用非捕获群组来表示:

 $(p{Alnum}+(?:\s+\p{Alnum}+)*)\s+([A-Z]{3})([0-9.]*)$ 

或者,采用更好的方式,按照名字捕获:

(?<item>\p{Alnum}+(\s+\p{Alnum}+)\*)\s+(?<currency>[A-Z]{3})(?<price>[0-9.]\*)

这样,就可以使用名称来获取产品了:

item = matcher.group("item");

用 start 和 end 方法可以获得输入中各个群组的位置:

```
int itemStart = matcher.start("item");\nint itemEnd = matcher.end("item");
```

- 警告: 按名称获取群组只对 Matcher 有效, 对 MatchResult 无效。
- 註釋:如果群组中包含重复內容,例如上面示例中的(\s+\p{Alnum}+)\*,那么我们将无法获得其所有匹配。group方法只能产生最后一个匹配,这几乎就没什么用处。我们需要用另一个群组来捕获完整的表达式。
- ☑ 提示: 我们可以在正则表达式中添加注释。注释以#开头,直至该行末尾。这种注释 方式特别适合文本块:

```
var regex = """
([1-9]|1[0-2]) #hours
:([0-5][0-9]) #minutes
[ap]m""";
```

程序清单 2-7 的程序提示输入一个模式,然后提示输入用于匹配的字符串,随后打印出输入是否与该模式相匹配。如果输入匹配模式并且模式包含群组,那么这个程序将用括号打印出群组边界,例如:

((11):(59))am

#### 程序清单 2-7 regex/RegexTest.java

```
package regex;

/**

* This program tests regular expression matching. Enter a pattern and strings to match,

* or hit Cancel to exit. If the pattern contains groups, the group boundaries are displayed

* in the match.

* @version 1.03 2018-05-01

* @author Cay Horstmann

*/
```

```
18
import java.util.*;
   import java.util.regex.*;
13
   public class RegexTest
14
15
      public static void main(String[] args) throws PatternSyntaxException
16
17
         var in = new Scanner(System.in);
18
         System.out.println("Enter pattern: ");
19
         String patternString = in.nextLine();
20
21
         Pattern pattern = Pattern.compile(patternString);
22
23
         while (true)
24
          {
25
             System.out.println("Enter string to match: ");
26
             String input = in.nextLine();
27
             if (input == null || input.equals("")) return;
28
             Matcher matcher = pattern.matcher(input);
29
             if (matcher.matches())
BE
31
                System.out.println("Match");
32
                int g = matcher.groupCount();
33
                if (q > 0)
34
35
                   for (int i = 0; i < input.length(); i++)
36
37
                      // Print any empty groups
38
                      for (int j = 1; j <= g; j++)
39
                         if (i == matcher.start(i) && i == matcher.end(i))
48
                             System.out.print("()");
41
                      // Print ( for non-empty groups starting here
42
                      for (int j = 1; j \le g; j++)
43
                         if (i == matcher.start(j) && i != matcher.end(j))
44
                             System.out.print('(');
45
                      System.out.print(input.charAt(i));
46
                      // Print ) for non-empty groups ending here
47
                      for (int j = 1; j \leftarrow g; j++)
48
                          if (i + 1 != matcher.start(j) && i + 1 == matcher.end(j))
49
                             System.out.print(')');
58
51
52
                   System.out.println();
                }
53
54
             else
55
                System.out.println("No match");
56
57
      }
58
59 }
```

#### 2.7.5 用分隔符来分割

有时,需要将输入按照匹配的分隔符断开,而其他部分保持不变。Pattern.split 方法可

以自动完成这项任务。调用此方法后可以获得一个剔除分隔符之后的字符串数组:

```
String input = . . .;
Pattern commas = Pattern.compile("\\s*,\\s*");
String[] tokens = commas.split(input);
    // "1, 2, 3" turns into ["1", "2", "3"]
如果有多个标记,那么可以惰性地获取它们:
```

Stream<String> tokens = commas.splitAsStream(input);

如果不关心预编译模式和惰性获取,那么可以使用 String.split 方法:

String[] tokens = input.split("\\s\*,\\s\*");

如果输入数据在文件中,那么需要使用扫描器:

```
Scanner in = new Scanner(path, "UTF_8");\nin.useDelimiter("\\s*,\\s*");
Stream<String> tokens = in.tokens();
```

#### 2.7.6 替换匹配

如果想要用某个字符串来替换正则表达式的所有匹配,那么可以在匹配器上调用 replaceAll 方法:

```
Matcher matcher = commas.matcher(input);
String result = matcher.replaceAll(",");
// Normalizes the commas
```

或者,如果不关心预编译模式,那么可以使用 String 类的 replaceAll 方法。

String result = input.replaceAll("\\s\*,\\s\*", ",");

替换字符串可以包含群组编号 \$n 或 \${name}。它们会被对应捕获到的组的内容所替换。

```
String result = "3:45".replaceAll(
  "(\\d{1,2}):(?<minutes>\\d{2})",
  "$1 hours and ${minutes} minutes");
// Sets result to "3 hours and 45 minutes"
```

你可以使用\来转义替换字符串中的\$和\,或者调用Matcher.quoteReplacement 这个便捷方法: matcher.replaceAll(Matcher.quoteReplacement(str))

如果想要执行比按照群组匹配拼接更复杂的操作,可以提供一个替换函数而不是替换字符串。该函数接受一个 MatchResult 对象,并会产生一个字符串。例如,在下面的代码中,我们将所有单词都替换为至少 4 个字母转换为大写形式的版本:

```
String result = Pattern.compile("\\pL{4,}")
   .matcher("Mary had a little lamb")
   .replaceAll(m -> m.group().toUpperCase());
   // Yields "MARY had a LITTLE LAMB"
```

replaceFirst 方法将只替换模式的第一次出现。

## 2.7.7 标志

有若干个标志(flag)都可以改变正则表达式的行为。可以在编译模式时设置标志:

Pattern pattern = Pattern.compile(regex,
 Pattern.CASE INSENSITIVE | Pattern.UNICODE CHARACTER CLASS);

或者, 可以在模式中指定它们:

String regex = "(?iU:expression)";

下面是各个标志。

- Pattern.CASE\_INSENSITIVE或i: 匹配字符时忽略字母的大小写,默认情况下,这个标志只考虑US ASCII字符。
- Pattern.UNICODE\_CASE 或 u: 当与 CASE\_INSENSITIVE 组合使用时,用 Unicode 字母的大小写来匹配。
- Pattern.UNICODE\_CHARACTER\_CLASS 或 U: 选择 Unicode 字符类代替 POSIX, 其中蕴含了 UNICODE CASE。
- Pattern.MULTILINE或 m: ^ 和 \$ 匹配行的开头和结尾, 而不是整个输入的开头和结尾。
- Pattern.UNIX LINES或d: 在多行模式中匹配个和\$时,只有'\n'被识别成行终止符。
- Pattern.DOTALL 或 s: 当使用这个标志时, . 符号匹配所有字符, 包括行终止符。
- Pattern.COMMENTS或x: 空白字符和注释(从#到行末尾)将被忽略。
- Pattern.LITERAL: 该模式将被逐字地采纳,必须精确匹配,因字母大小写而造成的差异除外。
- Pattern.CANON\_EQ:考虑 Unicode 字符规范的等价性,例如, u 后面跟随 "(分音符号) 匹配 ü。

最后两个标志不能在正则表达式内部指定。

# API java.util.regex.Pattern 1.4

- static Pattern compile(String expression)
- static Pattern compile(String expression, int flags)
  把正则表达式字符串编译到一个用于快速处理匹配的模式对象中。flags 参数是 CASE\_INSENSITIVE、UNICODE\_CASE、MULTILINE、UNIX\_LINES、DOTALL 和 CANON\_EQ 标志中的一个。
- Matcher matcher(CharSequence input)
   返回一个 matcher 对象,你可以用它在输入中定位模式的匹配。
- String[] split(CharSequence input)
- String[] split(CharSequence input, int limit)
- Stream<String> splitAsStream(CharSequence input) 8
  将输入分割成符号,其中模式指定了分隔符的形式。返回标记数组,分隔符并非符号的一部分。第二种形式有一个名为 limit 的参数,表示所产生的字符串的最大数量。如果已经发现了 limit-1个匹配的分隔符,那么返回的数组中的最后一项就包含所有剩余未分割的输入。如果 limit ≤ 0,那么整个输入都被分割;如果 limit 为 0,那么结尾的空字符串将不会置于返回的数组中。

#### API java.util.regex.Matcher

- boolean matches()如果输入匹配模式,则返回 true。
- boolean lookingAt()
   如果输入的开头匹配模式,则返回 true。
- boolean find()
- boolean find(int start)
   尝试查找下一个匹配,如果找到了另一个匹配,则返回 true。
- int start()
- int end() 返回当前匹配的开始索引和结尾之后的索引位置。
- String group()返回当前的匹配。
- int groupCount()返回输入模式中的群组数量。
- int start(int groupIndex)
- int start(String name) 8
- int end(int groupIndex)
- int end(String name) 8

返回当前匹配中给定群组的开始和结尾之后的位置。群组是由从1开始的索引指定的,或者用0表示整个匹配,或者用表示具名群组的字符串来指定。

- String group(int groupIndex)
- String group(String name)
   返回匹配给定群组的字符串。该群组是由从1开始的索引指定的,或者用0表示整个匹配,或者用表示具名群组的字符串来指定。
- String replaceAll(String replacement)
- String replaceFirst(String replacement)

返回从匹配器输入获得的通过将所有匹配或第一个匹配用替换字符串替换之后的字符串。 替换字符串可以包含用 \$n 表示的对群组的引用,这时需要用\\$来表示字符串中包含 一个 \$ 符号。

- static String quoteReplacement(String str) 5.0
   引用 str 中的所有\和\$。
- String replaceAll(Function MatchResult, String > replacer) 9 将每个匹配都替换为 replacer 函数应用于 MatchResult 上所产生的结果。
- Stream<MatchResult> results() 9 产生一个包含所有匹配结果的流。

#### API java.util.regex.MatchResult

- String group()
- String group(int group) 产生匹配的字符串,或者匹配给定群组的字符串。
- int start()
- int end()
- int start(int group)
- int end(int group) 产生匹配字符串或匹配给定群组的字符串的开始与结尾的偏移量。

#### API java.util.Scanner 5.0

• Stream<MatchResult> findAll(Pattern pattern) 9 产生一个流,其中包含了这个扫描器所产生的输入中针对给定模式的所有匹配。

你现在已经看到了在 Java 中输入输出操作是如何实现的,也对作为"新 I/O"规范一部分的正则表达式有了概略的了解。在下一章中,我们将转而研究对 XML 数据的处理。

# 第3章 XML

- ▲ XML 概述
- ▲ XML 文档的结构
- ▲ 解析 XML 文档
- ▲ 验证 XML 文档
- ▲ 使用 XPath 来定位信息

- ▲ 使用命名空间
- ▲ 流机制解析器
- ▲ 生成 XML 文档
- ▲ XSL 转换

Don Box 等人在其合著的 Essential XML (Addison-Wesley 出版社 2000 年出版)的前言中半开玩笑地说道: "可扩展标记语言(Extensible Markup Language,XML)已经取代了 Java、设计模式、对象技术,成为软件行业解决世界饥荒的方案。"这种炒作早就不新鲜了,但是正如你将在本章中看到的,XML 是一种非常有用的描述结构化信息的技术。XML 工具使处理和转化信息变得十分容易。但是,XML 并不是万能药,我们需要领域相关的标准和代码库才能有效地使用 XML。此外,XML 非但没有使 Java 技术过时,还与 Java 配合得很好。从 20 世纪 90 年代末以来,IBM、Apache 和其他许多公司一直在帮助开发用于 XML 处理的高质量 Java 库,其中大部分重要的代码库都整合到了 Java 平台中。

本章将介绍 XML, 并涵盖了 Java 库的 XML 特性。一如既往, 我们将指出何时大量地使用 XML 是正确的; 而何时必须有保留地使用 XML, 通过利用良好的设计和代码, 来采用老办法解决问题。

# 3.1 XML 概述

在卷 I 第 9 章中, 你已经看见过用属性文件 (property file)来描述程序配置。属性文件包含了一组名 / 值对, 例如:

fontname=Times Roman fontsize=12 windowsize=400 200 color=0 50 100

可以用 Properties 类在单个方法调用中读入这样的属性文件。这是一个很好的特性,但这还不够。在许多情况下,想要描述的信息的结构比较复杂,属性文件不能很方便地处理它。例如,对于下面例子中的 fontname/fontsize 项,使用以下的单一项将更符合面向对象的要求:

font=Times Roman 12

但是,这时对字体描述的解析就变得很讨厌了,必须确定字体名在何处结束,字体大小

在何处开始。

属性文件采用的是一种单层平面结构。你常常会看到程序员用如下的键名来努力解决这种局限性:

```
title.fontname=Helvetica
title.fontsize=36
body.fontname=Times Roman
body.fontsize=12
```

属性文件格式的另一个缺点是要求键是唯一的。如果要存放一个值序列,则需要另一个 变通方法,例如:

```
menu.item.1=Times Roman
menu.item.2=Helvetica
menu.item.3=Goudy Old Style
```

XML 格式解决了这些问题,因为它能够表示层次结构,这比属性文件的平面表结构更灵活。 描述程序配置的 XML 文件可能会像这样:

```
<config>
   <entry id="title">
      <font>
         <name>Helvetica</name>
         <size>36</size>
      </font>
   </entry>
   <entry id="body">
      <font>
         <name>Times Roman</name>
         <size>12</size>
      </font>
   </entry>
   <entry id="background">
      <color>
         <red>0</red>
         <green>50</green>
         <blue>100</blue>
      </color>
   </entry>
</config>
```

XML 格式能够表达层次结构,并且允许在确保格式不走样的情况下记录重复元素。

XML 文件的格式非常直观,它与 HTML 文件非常相似。这是有原因的,因为 XML 和 HTML 格式是古老的标准通用标记语言(Standard Generalized Markup Language, SGML)的衍生语言。

SGML 从 20 世纪 70 年代开始就用于描述复杂文件的结构。它的使用在一些要求对海量文献进行持续维护的产业中取得了成功,特别是在飞机制造业中。但是,SGML 相当复杂,所以它从未风行。造成 SGML 如此复杂的主要原因是 SGML 有两个相互矛盾的目标。它既想要确保文档能够根据其文档类型的规则来形成,又想要通过可以减少数据键人的快捷方式使数据项变得容易表示。XML 设计成了一个用于因特网的 SGML 的简化版本。和通常情况一样,越简单的东西越好,XML 立即得到了长期以来一直在躲避 SGML 的用户的热情追捧。

**注释**: 在 http://www.xml.com/axml/axml.html 处可以找到一个由 Tim Bray 注解的 XML 标准的极佳版本。

尽管 HTML 和 XML 同宗同源, 但是两者之间存在着重要的区别:

- 与 HTML 不同, XML 是大小写敏感的。例如, <H1> 和 <h1> 是不同的 XML 标签。
- 在HTML中,如果从上下文中可以分清哪里是段落或列表项的结尾,那么结束标签 (如 或 
   就可以省略,而在XML中结束标签绝对不能省略。
- 在 XML 中,只有单个标签而没有相对应的结束标签的元素必须以/结尾,比如 <img src="coffeecup.png"/>。这样,解析器就知道不需要查找 </img> 标签了。
- 在 XML 中,属性值必须用引号括起来。在 HTML 中,引号是可有可无的。例如, <img src="my hamster.png"width=300 height=300> 对 HTML 来说是合法的,但是对 XML 来说则是不合法的。在 XML 中,必须使用引号,比如,width= "300"。
- 在HTML中,属性名可以没有值。例如,<input type="radio" name="language" value= "Java" checked>。在XML中,所有属性必须都有属性值。比如, checked= "true"或 checked= "checked"。
- 专门针对 HTML 4 和 5 而设计的 XML 称为 XHTML。

# 3.2 XML 文档的结构

XML 文档应当以一个文档头开始, 例如:

<?xml version="1.0"?>

或者

<?xml version="1.0" encoding="UTF-8"?>

严格来说,文档头是可选的,但是强烈推荐使用文档头。

直 注释:因为建立SGML是为了处理真正的文档,因此XML文件被称为文档,尽管许多XML文件是用来描述通常不被称作文档的数据集的。

文档头之后通常是文档类型定义 (Document Type Definition, DTD), 例如:

<!DOCTYPE web-app PUBLIC

"-//Sun Microsystems, Inc.//DTD Web Application 2.2//EN"

"http://java.sun.com/j2ee/dtds/web-app 2 2.dtd">

文档类型定义是确保文档正确的一个重要机制,但是它不是必需的。我们将在本章的后面讨论这个问题。

最后,XML 文档的正文包含根元素,根元素包含其他元素。例如:

<?xml version="1.0"?>

<!DOCTYPE config . . .>

<config>

```
<entry
      <font>
         <name>Helvetica</name>
         <size>36</size>
      </font>
   </entry>
   攀 _
</config>
```

*元 可以有子元 (child element) 文本或两 有。在上 例子中 font元 有两个 子元 它们是name和size name<sup>元</sup> 包含文本"Helvetica"。*

*提 在设计XML文档 构时 最好 元 么包含子元 么包含文本。换句 你应该避免下面的情况*

```
<font>
   Helvetica
   <size>36</size>
</font>
```

*在XML规范中 叫作混合式内容(mixed content)。在本 中 后你将会 到 如果 免了混合式内容 就可以 化 析 。*

*XML元 可以包含属性 例如*

*<size unit="pt">36</size>*

*何时 元 何时 属性 在XML设计人员中存在一些分歧。例如 将font做如下 描*

*<font nai»e«MHelvetica" size="36'7>*

*似乎比下 描 更 单一些*

```
<font>
   <name>Helvetica</name>
   <size>36</size>
</font>
```

*但是 属性 灵活性 差很多。假 你想把单位添加到size 值中去 如果使 属性 么 就必 把单位添加到属性值中去*

*<font name="HeU/etica size="36 pt"/>*

*嗨 在必 对字 串"36 pt" 析 正是XML 来 免 烦。 向size元 中添加一个属性 来会清晰得多*

```
<font>
   <name>Helvetica</name>
   <size unit=-pf>36</size>
</font>
```

*一条常 法则是 属性只应 来修改值 不是 来指定值。如果你发 ft己 人丫争 在 于某个 是否是对某个值 所做 修改 么你就应 对* *属性 "不" 转而使 元 多有 文档根本就不使 属性。*

*0 <sup>注</sup> <sup>在</sup>HTML<sup>中</sup> 属性 使用规则很 <sup>单</sup> 凡是不显 <sup>在</sup> <sup>上</sup> 是属性。例如 在下 接中*

*<a href="http://java.sun.com">Java Technology</a>*

*字 串Java Technology 在 上显 但是 个 接 URL并不是显示页面的 一 分。然 个 则对于大多數XML并不 么 因为XML文件中 数据并 像 常意义 样是 人浏览的。*

*元 和文本是XML文档"主 支撑 " 你可 会 到 其他一些标 明如下*

*字 引 (character reference) 形式是十 制值 或十六 制值;。例如 <sup>字</sup> 6可以 下 两 形式*

*W233; S#xE9;*

*实体引 (entity reference) 形式是&name .。下 些实体引*

*&U; &gt &anp; &quot; '*

*<sup>有</sup> 定义 含义 小于、大于、&、引号、 <sup>号</sup> <sup>字</sup> 。 可以在DTD中定 义其他 实体引 。*

*• CDATA 分(CDATA Section) <![CDATA[和】】>来 定其 。它们是字 数据 一 殊形式。可以使 它们来囊括 些含有<、>、&之 字 字 串 不必将 它们 为标 例如*

*<![CDATA[< & > are ny favorite delimiters!]>*

*CDATA 分不 包含字 串]]>。使用这一 性时要特别小心 因为它常 來当 作将遗留数据偷偷 入XML文档 一个后 。*

*处 指令(processing instruction)是 些专 在处 XML文档 应 序中使 指令 它们 <?和 >来 定其 例如*

*<?xinVstylesheet href-"mystyle.css<sup>w</sup> type= text/css\_7>*

*每个XML 以一个处 指令开头*

*<?xml version=B1.0"?>*

*注 (comment) <! 和 > 定其界限 例如*

*<!- This is <sup>a</sup> comment. -•>*

*注 不应 含有字 串-。注 应 只包含提供 文档 信息 其中 不应 含有 命令 命令应 是 处 指令来实 。*

# *3.3 <sup>析</sup>XML文档*

*处 XML文档 就 先 析(parse)它。 析器是 样一个 序 它 入一个文件,*

*个文件具有正 格式 然后将其分 成各 元 使得 序员 够 些元 。 Java库提供了两 XML 析器*

- *像文档对 模型(Document Object Model, DOM) 析器 样 树型 析器(tree parser),它们将 人 XML文档 换成树 构。*
- *<sup>像</sup>XML <sup>单</sup>API (Simple API for XML, SAX) 析器 <sup>样</sup> 流机制 析器(streaming parser),它们在 人XML文档时 成 应 事件。*

*DOM 析器对于实 我们 大多数 来 更容易一些 所以我们 先介 它。如 果 处 很 文档 它 成树 构将会消 大 内存 或 如果只是对于某些元 感兴 不关心它们 上下文 么在 些情况下应 使 流机制 析器。更多 信息可 以査 3.7 。*

*DOM 析器 接口已 W3C标准化了。org.w3c.dom包中包含了 些接口 型 定 义 比如 Document和Element 。不同 提供 比如Apache组织和IBM, 写了实 些接口 DOM 析器。Java XML 处 API ( Java API for XML Processing, JAXP)库使得 我们可以以插件形式使 些 析器中 任意一个。但是JDK中也包含了从Apache 析器 导出 D0M 析器。*

*要读入一个XML文档 先需要一个DocumentBuilder对 可以从DocumentBuilder Factory中得到 个对 例如*

*DocuinentBuilderFactory factory = DocumentBuilderFactory. newlnstance(); DocumentBuilder builder <sup>=</sup> factory.newDocumentBuilder();*

*在 可以从文件中 入某个文档*

*File <sup>f</sup> =… Document doc = builder.parse(f);*

*或 可以 一个URL来 人*

*URL <sup>u</sup> =.. Document doc <sup>=</sup> builder.parse(u.toString());*

*可以从任意一个指定 入流中 入*

*InputStream in =.. Document doc = builder.parse(in);*

*El<sup>注</sup> 如果使 榆入流作为 入源 么对于 些以 文档 <sup>位</sup> <sup>为</sup> <sup>对</sup> 径而被 引用的文档 析器将无法定位 比如在同一个 录中 DTD 但是 可以通过 安 一个"实体 析器"(entity resolver)来 决 个 。 查 www.xml.com/pub/ a/2004/03/03/catalogs.html 或 www.ibm.com/deveUjperworks/xmlJlibrary/x-inxd3.html,以 了 更多信息。*

*Document对 是XML文档 树型 构在内存中 方式 它 实 了 Node接口及其 各 子接口 对 构成。图3-1显 了各个子接口 层次 构。*

![](_page_143_Figure_2.jpeg)

*3-1 Node接口及其子接口*

*可以 getDocumentElement方法来启动对文档内容 分析 它将 回根元 。*

*Element root <sup>=</sup> doc.getDocumentElement();*

*例如 如果 处 下 文档*

```
<?xml version="1.8"?>
<font>
</font>
```

*么 getDocumentElement方法可以 回font元 。*

*getTagName方法可以 回元 标 名。在前 个例子中 root.getTagName() 回字 串"font"。*

*如果 得到 元 子元 (可 是子元 、文本、注 或其他 点) 使 get-ChildNodes方法 个方法会 回一个 型为NodeList的集合。 个 型在标准 Java 合 创建之前就已 标准化了 因此它具有一 不同 协 item方法将得到指定 引 值的项 getLength方法则提供了项的总数。因此 我们可以像下面这样枚举所有子元*

```
NodeList children = root.getChildNodesO;
for (int i = 0; i < children.getLength(); i-n)
{
   Node child = children.item(i);
     會
}
分析子元 时 很仔 。例如 假 你正在处 以下文档
<font>
   <name>Helvetica</name>
   <size>36</size>
</font>
```

*你 期font有两个子元 但是 析器却报告 有5个:*

- *• font <sup>和</sup> (<sup>116</sup> 之间的空白字*
- *• name元*
- *• /name 和 size 之 字*
- *• size元*
- *• /size 和 /font 之 字*

*图3-2显 了其DOM树。*

![](_page_144_Figure_8.jpeg)

*如果只希望得到子元 么可以忽略空白字*

```
for (int i = 6; i children.getLength(); i++)
{
   Node child = children.item(i);
   if (child instanceof Eleiwnt childElement)
   {
      • • •
   }
}
```

*在 只会 到两个元 它们 标 名是name和size*

*正如将在下一 中所 到 样 如果你 文档有DTD, 么你就可以做得更好。 时 析器 哪些元 没有文本 点 子元 且它会帮你剔 字 。*

*在分析name和size元 时 你 定想 取它们包含 文本字 串。 些文本字 串本 身都包含在Text 型 子 点中。既然 了 些Text 点是唯一 子元 就可以 getFirstChild方法 不 再 历另一个NodeList。然后可以 getData方法 取存储在Text 点中 字 串。*

```
for (int i = 0; i < children.getLength(); i++)
{
   Node child = children.item(i);
   if (child instanceof Element childElement)
   {
      var textNode = (Text) childElement.getFirstChild();
      String text = textNode.getData().strip();
      if (childElement.getTagName().equals("name"))
           name = text;
      else if (childElement.getTagName().equals("size"))
           size = Integer.parseInt(text);
   }
}</pre>
```

√ 提示: 对 getData 的返回值调用 trim 方法是个好主意。如果 XML 文件的作者将起始和结束的标签放在不同的行上,例如:

```
<size>
36
</size>
```

那么,解析器将会把所有的换行符和空格都包含到文本节点中去。调用 trim 方法可以 把位于实际数据前后的空白字符删掉。

也可以用 getLastChild 方法得到最后一项子元素,用 getNextSibling 得到下一个兄弟节点。这样,另一种遍历子节点集的方法就是:

```
for (Node childNode = element.getFirstChild();
     childNode != null;
     childNode = childNode.getNextSibling())
{
     . . .
}
```

如果要枚举节点的属性,可以调用 getAttributes 方法。它返回一个 NamedNodeMap 对象,其中包含了描述属性的 Node 对象。可以用和遍历 NodeList 一样的方式在 NamedNodeMap 中遍历各子节点。然后,调用 getNodeName 和 getNodeValue 方法可以得到属性名和属性值。

```
NamedNodeMap attributes = element.getAttributes();
for (int i = 0; i < attributes.getLength(); i++)
{
   Node attribute = attributes.item(i);
   String name = attribute.getNodeName();
   String value = attribute.getNodeValue();
   . . . .
}</pre>
```

或者,如果知道属性名,则可以直接获取相应的属性值:

String unit = element.getAttribute("unit");

现在你已经知道怎么分析 DOM 树了。程序清单 3-1 中的程序将这些技术都运用了一遍,将一个 XML 文档转换成了 JSON 格式。

该树形结构清楚地显示了子元素是怎样被包含空白字符和注释的文本包围起来的。你可以清楚地看到换行符和回车符显示成了 \n。

无须熟悉 JSON 就可以理解这个程序是如何操作 DOM 树的, 你只需观察以下几点:

- 我们使用了一个 DocumentBuilder 来从文件中读取一个 Document。
- 对于每一个元素, 我们打印了标签名、属性和元素。
- 对于字符数据,我们用这些数据产生了一个字符串。如果数据来自于注释,那么我们就会添加 "Comment:" 前缀。

#### 程序清单 3-1 dom/JSONConverter.java

```
1 package dom;
2
3 import java.io.*;
4 import java.util.*;
  import javax.xml.parsers.*;
8 import org.w3c.dom.*;
   import org.xml.sax.*;
10
11 /**
   * This program displays an XML document as a tree in JSON format.
   * @version 1.21 2021-05-30
    * @author Cay Horstmann
15
16 public class JSONConverter
17
   {
      public static void main(String[] args)
18
            throws SAXException, IOException, ParserConfigurationException
19
28
         String filename;
21
         if (args.length == 0)
22
23
            try (var in = new Scanner(System.in))
24
25
               System.out.print("Input file: ");
26
               filename = in.nextLine();
27
28
         }
29
         else
38
             filename = args[0];
31
         DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
32
         DocumentBuilder builder = factory.newDocumentBuilder():
33
34
         Document doc = builder.parse(filename);
35
36
         Element root = doc.getDocumentElement();
         System.out.println(convert(root, 0));
37
38
39
      public static StringBuilder convert(Node node, int level)
40
41
         if (node instanceof Element elem)
42
```

```
134
```

```
43
         {
            return elementObject(elem, level);
44
45
         else if (node instanceof CharacterData cd)
47
            return characterString(cd, level);
48
49
         else
58
51
         {
            return pad(new StringBuilder(), level).append(
52
               jsonEscape(node.getClass().getName()));
53
54
      }
55
56
      private static Map<Character, String> replacements = Map.of('\b', "\\b", '\f', "\\f",
57
          '\n', "\\n", '\r', "\\r", '\t", "\\t", "\\\"", '\\\");
58
59
60
      private static StringBuilder jsonEscape(String str)
61
         var result = new StringBuilder("\"");
62
         for (int i = 0; i < str.length(); i++)
63
            char ch = str.charAt(i);
65
            String replacement = replacements.get(ch);
            if (replacement == null) result.append(ch);
67
            else result.append(replacement);
68
         result.append("\"");
78
71
         return result:
72
73
      private static StringBuilder characterString(CharacterData node, int level)
74
75
         var result = new StringBuilder();
76
77
         StringBuilder data = jsonEscape(node.getData());
          if (node instanceof Comment) data.insert(1, "Comment: ");
78
         pad(result, level).append(data);
79
          return result;
81
82
      private static StringBuilder elementObject(Element elem, int level)
83
84
          var result = new StringBuilder();
85
          pad(result, level).append("{\n");
          pad(result, level + 1).append("\"name\": ");
87
          result.append(jsonEscape(elem.getTagName()));
88
          NamedNodeMap attrs = elem.getAttributes();
          if (attrs.getLength() > \theta)
98
          1
91
             pad(result.append(",\n"), level + 1).append("\"attributes\": ");
             result.append(attributeObject(attrs));
93
94
          NodeList children = elem.getChildNodes();
95
          if (children.getLength() > 0)
96
97
```

```
98
99
IM
161
182
163
164
165
166
187
168
lie
in
126
127
128
129
136 }
             pad(result.append(",\n"), level + 1).append(B\"children\M: [\nM);
             for (int i = 0; i < children.getLength(h i-H)
             {
                if (i > B) result.append
                result.append(convert(children.item(i)r level + 2));
             }
             result.append(H\nB);
             pad(result, level + l).append(n]\n");
          }
          pad(result, level).append("}");
          return result;
      }
      private static StringBuilder pad(StringBuilder builder, int level)
      {
          for (int i = 0; i < level; i++) builder.a叩end("
          return builder;
      private static StringBuilder attributeObject(NamedNodeMap attrs)
      {
          var result = new StringBuilder("{■);
          for (int i = 0; i < attrs.getLengthO; i++)
          {
             if (i > 8) result.append(M, H);
             result.append(jsonEscape(attrs.item(i).getNodeName()));
             result.append(": ) 
             result, append (jsonEscape(attrs.iteffl(i) .getNodeValueO));
          }
          result.a叩end( }");
          return result;
      }
```

# *j avax.xml.parsers.DocunentBuilderFactory*

- *• static DocumentBuilderFactory newlnstance() 回 DocumentBuilderFactory 一个实例。*
- *• DocumentBuilder newDocumentBuilder() 回DocumentBuilder 一个实例。*

# *ah] javax.xml.parsers.DocumentBuilder*

- *• Document parse(File f)*
- *• Document parse(String url)*
- *• Document parsed叩utStream in) 析来 定文件、URL或 入流 XML文档 冋 析后 文档。*

# *奶<sup>j</sup> org.w3c.dom.Document*

*• Element getDocumentElement() 回文档 根元 。*

# *aw<sup>|</sup> org.w3c.don.Element*

- *• String getTagNameO 回元 名字。*
- *• String getAttribute(String name) 回 定名字 属性值 没有 属性时 回 字 串。*

#### *為叫 org.w3c.dom.Node*

- *• NodeList getChildNodesO 回包含该节点所有子元索的节点列 。*
- *• Node getFirstChildO*
- *• Node getLastChildO 取 点 一个或最后一个子 点 在 点没有子 点时 回null*
- *• Node getNextSiblingO*
- *• Node getPreviousSiblingO 取 点 下一个或上一个兄弟 点 在 点没有兄弟 点时 回nuU<sup>0</sup>*
- *• Node getParentNodeO 取 点 点 在该节点是文档 点时 回null*
- *• NamedNodeMap getAttributesO 回含有描 点所有属性 Attr 点 映射 。*
- *• String getNodeNameO 回 点 名字。当该节点是Attr 点时 名字就是属性名。*
- *• String getNodeValueO 回 点 值。当该节点是Attr 点吋 值就是属性值。*

# *<sup>a</sup>«] org.w3c.dom.CharacterData*

*• String getDataO 回存储在 点中 文本。*

# *org.w3c.dom.NodeList*

- *• int getLength() 回列 中 点数。*
- *• Node item(int index) 回 定 引值处 点。 引值 围在9到getLength()-l之 。*

#### *供<sup>i</sup> org.w3c. doin. NamedNodeMap*

- *• int getLength() 回 点映射 中 点数。*
- *• Node item(int index) 回 定 引值处 点。 引值 围在0到getLength()-l之 。*

# *3.4验证XML文档*

*在前一 中 我们了 了如何 历DOM文档 树形 构。然 如果仅仅按照 方 法来操作 会发 大 冗 和 检査工作。不但 处 元 字 还要检査 文档包含的节点是否和期望 一样。例如 在 入下 个元 时*

```
<font>
   <name>Helvetica</name>
   <size>36</size>
</font>
```

*将 先得到 一个子 点 是一个含有 字 "\n" 文本 点。跳过文本 点后找到 是 一个元 点。然后 检査它 标 名是不是"name",还要检査它是否有一个Text 型 子 点。接下来 到下一个非空白字符的子 点 并进行同样 检査。 么 当文档 作 改变了子元 序或是加人另一个子元 时又会怎样呢 是对所有 检查 就会显得太 烦了 些检査又显得不慎 。*

*幸好 XML 析器 一个很大 好处就是它 动校 某个文档是否具有正 构。 样 析就变得 单多了。例如 如果 font 段已 了 么不 一步检 查就 得到其两个孙 点 并把它们 换成Text 点 得到它们 文本数据。*

*如果 指定文档 构 可以提供一个文档 型定义 DTD 或一个XML Schema定义。 DTD或schema包含了 于 文档应如何构成 则 些 则指定了每个元素的合法子 元 和属性。例如 某个DTD可 含有一 则*

*<•ELEMENT font name,size >*

*则 一个font元 必 总是有两个子元 分别是name和size 将同样 束 XML Schema 如下*

```
<xsd:element name="font">
   <xsd:sequence>
      <xsd:element name="name_ type=,,xsd:string'7>
      <xsd:element name="size type="xsd:int7>
   </xsd:sequence>
</xsd:element>
```

*与DTD 比 XML Schema可以 更加复杂 条件 比如size元 必 包含一 个整数 。与DTD 法不同 XML Schema 使 就是XML, 为处 Schema文件带 来了方便。*

*在下一 中 我们将 DTD 接 介 XML Schema 一些基 。最 后 我们会展 一个完整 应 序来演 是如何 化XML编程的。*

# *3.4.1文档 型定义*

*提供DTD 方式有多 。可以像下面这样将其 入XML文档中*

```
<?xml version="1.0 > 
<!DOCTYPE config [
```

```
<!ELEMENT config . . .>
more rules

. . .

|>
<config>
. . .
</config>
```

正如你看到的,这些规则被纳入 DOCTYPE 声明中,位于由 [...] 限定界限的块中。文档类型必须匹配根元素的名字,比如我们例子中的 configuration。

在 XML 文档内部提供 DTD 不是很普遍,因为 DTD 会使文件长度变得很长。把 DTD 存储在外部会更具意义,SYSTEM 声明可以用来实现这个目标。可以指定一个包含 DTD 的 URL,例如:

<!DOCTYPE config SYSTEM "config.dtd">

或者

<!DOCTYPE config SYSTEM "http://myserver.com/config.dtd">

● 警告:如果使用的是DTD的相对URL(比如 "config.dtd"),那么要给解析器一个File或URL对象,而不是InputStream。如果必须从一个输入流来解析,那么请提供一个实体解析器(请看下面的说明)。

最后,有一个来源于 SGML 的用于识别"众所周知的"DTD 的机制,下面是一个例子:

<! DOCTYPE web-app

PUBLIC "-//Sun Microsystems, Inc.//DTD Web Application 2.2//EN" "http://java.sun.com/j2ee/dtds/web-app 2 2.dtd">

如果 XML 处理器知道如何定位带有公共标识符的 DTD, 那么就不需要 URL 了。

i 注释: DTD 的系统标识符 URL 可能实际无法工作,或者会显著地降低性能。后者有一个例子,即 XHTML1.0 Strict DTD 的系统标识符,可以在 http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd 处找到它的信息。如果要解析一个 XHTML 文件,可能会花费一两分钟来处理 DTD。

有一种解决方案是使用**实体解析器**,它会将公共标识符映射为本地文件。在 Java 9 之前,我们不得不提供一个实现了 EntityResolver 接口并实现了 resolveEntity 方法的某个类的对象。

但是,现在我们可以使用 XML 目录来管理这种映射。我们需要提供一个或多个 具有下面这种形式的目录文件:

<?xml version="1.0"?>
<!DOCTYPE catalog PUBLIC "-//OASIS//DTD XML Catalogs V1.0//EN"
 "http://www.oasis-open.org/committees/entity/release/1.0/catalog.dtd">
<catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog" prefer="public">
 <public publicId="..." uri="..."/>

</catalog>

然后像下面这样构造和安装一个解析器:

builder.setEntityResolver(CatalogManager.catalogResolver(
 CatalogFeatures.defaults(),
 Paths.get("catalog.xml").toAbsolutePath().toUri()));

请参阅程序清单3.6中完整的示例。

除了在程序中设置目录文件的位置,还可以在命令行中用 javax.xml.catalog.files 系统属性来设置它,我们需要提供由分号分隔的 file 的绝对 URL。

既然你已经知道解析器怎样定位 DTD 了,那么下面就让我们来看看不同种类的规则。 ELEMENT 规则用于指定某个元素可以拥有什么样的子元素。可以指定一个正则表达式, 它由表 3-1 中所示的组成部分构成。

| 规则                                | 含 义                                               |  |
|-----------------------------------|---------------------------------------------------|--|
| E*                                | 0 或多个 E                                           |  |
| E+                                | 1 或多个 E                                           |  |
| E?                                | 0或1个E                                             |  |
| $E_1 E_2 \cdots E_n$              | $E_1, E_2, \cdots, E_n$ 中的一个                      |  |
| $E_1, E_2, \cdots, E_n$           | $E_1$ 后面跟着 $E_2, \cdots, E_n$                     |  |
| #PCDATA                           | 文本                                                |  |
| $(\#PCDATA E_1 E_2 \cdots E_n)^*$ | $0$ 或多个文本且 $E_1, E_2, \cdots, E_n$ 以任意顺序排列(混合式内容) |  |
| ANY                               | 允许有任意子元素                                          |  |
| EMPTY                             | 不允许有子元素                                           |  |

表 3-1 用于元素内容的规则

下面是一些简单而典型的例子。下面的规则声明了 menu 元素包含 0 或多个 item 元素:

<!ELEMENT menu (item)\*>

下面这组规则声明 font 是用一个 name 后跟一个 size 来描述的,它们都包含文本:

- <!ELEMENT font (name, size)>
- <!ELEMENT name (#PCDATA)>
- <!ELEMENT size (#PCDATA)>

缩写 PCDATA 表示被解析的字符数据。这些数据之所以被称为"被解析的"是因为解析器通过寻找表示一个新标签起始的 < 字符或表示一个实体起始的 & 字符,来解释这些文本字符串。

元素的规格说明可以包含嵌套的和复杂的正则表达式,例如,下面是一个描述了本书中每一章的结构的规则:

<!ELEMENT chapter (intro,(heading,(para|image|table|note)+)+)

每章都以简介开头,其后是1或多个小节,每个小节由一个标题和1个或多个段落、图片、表格或说明构成。

然而,有一种常见的情况是无法把规则定义得像你希望的那样灵活的。当一个元素可以 包含文本时,那么就只有两种合法的情况。要么该元素只包含文本,比如: *<!ELEMENT nane (#PCDATA)>*

*么 元 包含任意 序 文本和标 合 比如*

*<!ELEMENT para (#PCDATA|effi|strong|code)\*>*

*指定其他任何 型 包含#PCDATA 则 是不合法 。例如 以下 则是 法*

*<!ELEMENT captionedlmage (image,#PCDATA)>*

*必 写 则 以引人另一个名为caption 元 或 允 使 image元 和文本 任 意 合。*

*制 化了 XML 析器在 析混合式内容(标 和文本 混合)时 工作。因为在 允 使 混合式内容时 免会失控 所以最好在设计DTD时 其中所有 元 么包含 其他元 么只有文本。*

*注 实 上 在DTD 则中并不 为元 指定任意 正则表达式 XML 析器会 拒 某些导 定性 复杂 则。例如 正则表达式((xfy)|(x,z))就是 定性 。当 析器 到X时 它不 在两个 择中应 取哪一个。 个 式可以改 写成 定性 形式 如(x,(y|z)) 然 有一些 式不 改写 如( x,y)\*|x? Java XML库中 析器在 到有歧义 DTD时 不会 出 告。在 析时 它仅仅 在两 中 取 一个匹 将导 它会拒 一些正确的输入。当然 析器有权 么做 因为XML标准允 析器假 DTD 是 二义性 。*

*可以指定 于描 合法 元 属性 则 其 法为*

*<!ATTLIST element attribute type default>*

*3-2显 了合法 属性 型(type), 3-3显 了属性 值(default) 法。*

| 型                 | 含义                    |
|-------------------|-----------------------|
| CDATA             | 任意字<br>串              |
| …K)               | 串属性AXtAu…<br>字<br>人之一 |
| NMTOKEN, NMT0KENS | 1或多个名字<br>号           |
| ID                | 1个唯一<br>ID            |
| IDREF, IDREFS     | ID<br>1或多个对唯一<br>引    |
| ENTITY, ENTITIES  | 1或多个未<br>析实体          |

*3-2属性 <sup>型</sup>*

*3-3属性 <sup>值</sup>*

| 值        | 含义                                                     |  |
|----------|--------------------------------------------------------|--|
| SQUIRED  | 属性是必                                                   |  |
| •IMPLIED | 属性是可                                                   |  |
| A        | 属性是可<br>未指定<br>析器报告<br>属性是X                            |  |
|          | 是j<br>属性必<br>是未指定<br>或<br>是在<br>两<br>情况下<br>析器报告<br>属性 |  |

以下是两个典型的属性规格说明:

<!ATTLIST font style (plain|bold|italic|bold-italic) "plain"> <!ATTLIST size unit CDATA #IMPLIED>

第一个规格说明描述了 font 元素的 style 属性。它有 4 个合法的属性值,默认值是 plain。第二个规格说明表示 size 元素的 unit 属性可以包含任意的字符数据序列。

這程:一般情况下,我们推荐用元素而非属性来描述数据。按照这个推荐,字体的样式应该是一个单独的元素,例如<font><style>plain</style>...</font>。然而,对于枚举类型,属性有一个不可否认的优点,那就是解析器能够校验其取值是否合法。例如,如果字体的样式是一个属性,那么解析器就会检查它是不是4个允许的值之一,并且如果没有为其提供属性值,那么解析器还会为其提供一个默认值。

CDATA 属性值的处理与前面看到的对 #PCDATA 的处理有着微妙的差别,并且与 <! [CDATA [...]]> 部分没有多大关系。属性值首先被规范化,也就是说,解析器要先处理对字符和实体的引用(比如 &#233;或 &lt;),并且要用空格来替换空白字符。

NMTOKEN (即名字符号)与 CDATA 相似,但是大多数非字母或数字字符和内部的空白字符都是不允许使用的,而且解析器会删除开头和结尾的空白字符。NMTOKENS 是一个以空白字符分隔的名字符号列表。

ID 结构是很有用的, ID 是在文档中必须唯一的名字符号,解析器会检查其唯一性。在下一个示例程序中,你会看到它的应用。IDREF 是对同一文档中已存在的 ID 的引用,解析器也会对它进行检查。IDREFS 是以空白字符分隔的 ID 引用的列表。

ENTITY 属性值将引用一个"未解析的外部实体"。这是从 SGML 那里沿用下来的,在实际应用中很少见到。在 http://www.xml.com/axml/axml.html 处的被注解的 XML 规范中有该属性的一个例子。

DTD 也可以定义实体,或者定义解析过程中被替换的缩写。你可以在 Firefox 浏览器的用户界面描述中找到一个很好的使用实体的例子。这些描述被格式化为 XML 格式,包含了如下的实体定义:

<!ENTITY back.label "Back">

其他地方的文本可以包含对这个实体的引用,例如:

<menuitem label="&back.label;"/>

解析器会用替代字符串来替换该实体引用。如果要对应用程序进行国际化处理,只需修改实体定义中的字符串即可。其他的实体使用方法更加复杂,且不太常用,详细说明参见 XML 规范。

这样我们就结束了对 DTD 的介绍。既然你已经知道如何使用 DTD 了,那么你就可以配置你的解析器以充分利用它们了。首先,通知文档生成工厂打开验证特性。

factory.setValidating(true);

*样 工厂 成 所有文档 成器 将根据DTD来 它们 入。 最大好 处是可以忽 元 内容中的空白字 。例如 考虑下面的XML代 段*

```
<font>
   <name>Helvetica</name>
   <size>36</size>
</font>
```

*一个不 析器会报告font name和size元 之 字 因为它无法 font 子元 是*

```
(name,size)
(fPCDATA,name,size)*
```

*是*

*ANY*

*一旦DTD指定了子元 是(name,size), 析器就知道它们之间的空白字 不是文本。 下面的代*

*factory.setIgnoringElementContentWhitespace(true);*

*样 成器将不会报告文本 点中 字 。 意味 你可以依 font 点拥有2<sup>个</sup> 子元 一事实 再也不 写下 样 单 冗 循 代 了*

```
for (int i = i < children.getLength(); i++)
{
   Node child = children.iteni(i);
   if (child instanceof Element childElement)
   {
      if (childElement.getTagName().equals(■naffle0))..
      else if (childElement.getTagName().equals("size"))..
   }
}
```

*只 仅仅 如下代 一个和 二个子元*

```
var nameElement = (Element) children.iteni(0);
var sizeElement = (Element) children.item(1>;
```

*就是DTD如此有 原因。你不会为了检査 则 使 序 担 。在得到文档之 前 析器已 做完了 些工作。*

*当 析器报告 时 应 序希望对 执 某些操作。例如 录到日志中 把 它显 户 或是抛出一个异常以放弃 析。因此 只 使用验证 就应 安 一个 处 器 提供一个实 了 ErrorHandler接口 对 。 个接口有三个方法*

```
void warning(SAXParseException e)
void error(SAXParseException e)
void fatalError(SAXPa rseException e)
```

*可以 DocumentBuilder setErrorHandler方法来安 处 器*

```
builder.setErrorHandler(handler);
```

# *api<sup>|</sup> javax.xml• parsers• DocumentBuilder*

- *• void setEntityResolver(EntityResolver resolver) 设置解析器 来定位 析 XML文档中引 实体。*
- *• void setErrorHandler(ErrorHandler handler) 来报告在 析 中出 和 告 处 器。*

## *奶| org.xml.sax.EntityResolver*

*• public InputSource resolveEntity(String publicID, String systemlD) 回一个 入源 它包含了 定ID所引用的数据 或 当 析器不 如何 <sup>析</sup> <sup>个</sup> 定名字时 <sup>冋</sup>null 如果没有提供公共ID, 么参数publicID可以为 nuU<sup>o</sup>*

## *am] org.xml.sax.InputSource*

- *• InputSource(Inputstream in)*
- *• InputSource(Reader in)*
- *• InputSource(String systemlD) 从流、 人器或 ID ( 常是 对或 对URL)中构建 人源。*

# *gcr<sup>8</sup>.x#l.sax.ErrorHandler*

- *• void fatalError(SAXParseException exception)*
- *• void error(SAXParseException exception)*
- *• void warning(SAXPa rseException exception) 些方法以提供对 命 、 命 和 告 处 处 器。*

# *afi] o rg. xml. sax. SAXPa rseException*

- *• int getLineNumber()*
- *• int getColumnNumber() 回引 异常 已处 入信息末尾 号和列号。*

# *叫 javax.xil.catalog.CatalogManager*

*• static CatalogResolver catalogResolver(CatalogFeatures features, URI... uris) 产 一个 析器 它将使 所提供 URI指定 位 上 录文件。创建出来 析器所属 CatalogResolver 实 了 EntityResolver 接口 以及 StAX Schema 校 和XSL 换 到的解析器接口。*

# *aw<sup>|</sup> javax.xml.catalog.CatalogFeatures*

*• static CatalogFeatures defaults() 产 一个实例。*

# *APij| javax.xml. parsers. DocumentBuilderFactory*

- *• boolean isValidatingO*
- *• void setvalidating(boolean value) 取和 工厂 validating属性。当它 <sup>为</sup>true<sup>时</sup> T<sup>厂</sup> <sup>成</sup> 析器会 <sup>它</sup> 们 入信息。*
- *• boolean isIgnoringElementContentWhitespace()*
- *• void setIgnoringElementContentWhitespace(boolean value) 取和 工厂 ignoringElementContentWhitespace属性。当它 为true时 工 厂 成 析器会忽 不含混合内容(即元 与#PCDATA混合) 元 点之 字 。*

## *3.4.2 XML Schema*

*因为XML Schema比 DTD 法 复杂 多 所以我们只涉及其基本 。更多信息 参 http://www.w3.org/TR/xmlschema-0 上 指南。*

*如果 在文档中引 Schema文件 在根元 中添加属性 例如*

```
<?xml version="1.0"?>
<config xnlns:xsi=Nhttp://www•w3.org/2661/XMLSchema-instance"
      xsi:noNamespaceSchemaLocation="config.xsd">
</config>
```

*个声明 明Schema文件config.xsd会被用来验证该文档。如果使 命名 法 就更加复杂了。 <sup>情</sup> <sup>参</sup> XML Schema指南(前 xsi是一个命名 别名(namespace alias), 査 3.6 以了 更多信息)。*

*Schema为每个元 和属性 定义了 型。 型中 单 型是对内容有 制 字 串 其他 是复杂 型。具有 单 型 元 可以没有任何属性和子元 。否则 它就必然是复 杂 型。与此 反 属性总是 单 型。*

*一些 单 型已 内建到了 XML Schema内 包括*

```
xsd:string
xsd:int
xsd:boolean
```

*0 <sup>注</sup> 我们 <sup>前</sup> XSd:<sup>来</sup> XSL Schema定义 命名空间。一些作 代之以XS:<sup>0</sup>*

*可以定义 己 单 型。例如 下 是一个枚举 型*

```
<xsd:simpleType name="Styl.eType">
   <xsd:restriction base= xsd:string"
      <xsd:enumeration value="PLAIN" />
      <xsd:enumeration value="BOLD" />
      <xsdenumeration value="ITALIC" />
      <xsd:enumeration value="BOLD_ITALIC" />
   </xsd:restriction>
</xsd:simpleType>
```

```
当定义元 时 指定它 型
    <xsd:element name?name" type="xsd:string7>
    <xsd:element name= size* type="xsd:int"/>
    <xsd:element name= style" type="StyleType'7>
      型 束了元 内容。例如 下 元 将 为具有正 格式
    <size>l </size>
    <style>PLAIN</style>
    但是 下 元 会 析器拒
    <size>default</size>
    <style>SLANTED</style>
    可以把 型 合成复杂 型 例如
    <xsd:complexType name= FontTypett>
       <xsd:sequence
         <xsd:element ref="name"/>
         <xsd:element ref="size"/>
         <xsd:element ref="style7>
       </xsd:sequence>
    </xsd:coniplexType>
    FontType是name size和style元素的序列。在 个 型定义中 我们使 了 ref属性来
引 在Schema中位于别处 定义。也可以嵌套定义 像 样
    <xsd: complexType name= ** FontType・>
       <xsd:sequence>
         <xsd:element name=ttnameM type="xsd:string7>
         <xsd:element name="size" type="xsd:int"/>
         <xsd:element name=MstyleM>
            <xsd:simpleType>
              <xsd:restriction base="x$d:string">
                 <xsd:enumeration value="PLAIN" />
                 <xsd:enumeration value=MBOLD" />
                 <xsd:enumeration values'ITALIC' />
                 <xsd:enumeration value="BOLD ITALIC" />
              </xsd:restriction>
            </xsd:sinpleType>
         </xsd:element>
       </xsd:sequence
    </xsd:complexType>
      注意style元 匿名 型定义。
    xsd:sequence 构和DTD中的连接 号 价 xsd:choice 构和|操作 价 例如
     <xsd:complexType name="contactinfo">
       <xsd:choice>
         <xsd:element ref="efnailM/>
         <xsd:element ref=Mphone'7>
       </xsd:choice>
     </xsd:coniplexType>
```

*如果 允 复元 可以使 minoccurs和maxoccurs属性 例如 与DTD 型item\**

*和DTD中 型email <sup>|</sup> phone 型是 价 。*

## *价 形式如下*

*<xsd:element name="item1' type=".. minoccurs= 0" maxoccurs="unbounded'\*>*

*如果 指定属性 可以把xsd:attribute元 添加到complexlype定义中去*

*<xsd:element name="size"> <xsd:complexlype>*

*• • • <xsd:attribute name="unit" type="xsd: string" use= optionaV defaul>t=Mcm"/> </xsd:complexType> </xsd:element>*

# *与下面的DTD 句 价*

*<IATTLIST Size unit CDATA IMPLIED ■cm <sup>&</sup>gt;*

*可以把Schema 元 和 型定义封 在xsd:schema元 中*

*<xsd:schema xfnlns:xsd=Mhttp://www.w3.org/20ei/XMLScheflia',>*

*</xsd:schefia>*

*析带有Schema XML文件和 析带有DTD 文件 似 但有2点差别*

*1. 必 打开对命名 支持 即使在XML文件 可 不会 到它。*

*factory. setNaiwspaceAware(true);*

*2. 必 如下 " 咒"来准备好处 Schema 工厂。*

*final String JAXP\_SCHEMA\_LANGUAGE <sup>=</sup> "http://java•sun•con/xnl/jaxp/properties/schemaLanguageM; final String W3C\_XML\_SCHEMA <sup>=</sup> <sup>M</sup>http://www.w3.org/2❷❷l/XMLSchema'; factory.setAttribute7jAXP\_SCHEMA\_LANGUAGE, W3C XMLJCHEMA);*

# *3.4.3 —个实践示例*

*在本 中 我们将 介 一个实 例 序 来 明在实 境中XML的用法。 假 有一个应用程序需要配置数据 些数据可以指定任意对 不只是文本字 串。我们提供了两 机制来实例化对 使 构 器和使 工厂方法。下 展 了如何使 构 器来创建Color对*

*<construct class="j ava awt Color•> <int>55</int> <int>2❷❷</int> <int>10fl</int> </construct>*

*下 是使 工厂方法 例子*

*<factory classs"j ava.util.logging.Logger" method='getLogger'> <string>com.horstmann.core)ava</string> </factory>*

*如果忽 工厂方法名 么其 值就是getlnstance<sup>o</sup>*

*正如你所 有多个元 来描 字 串和整数。我们 支持boolean 型 其他基本*

类型也都可以按照相同的方式添加进来。

只是为了显摆一下, 我们给出了第二种针对基本类型的机制:

<value type="int">30</value>

配置是由多个项构成的序列。每一项都有一个 ID 和一个对象:

```
<config>
```

解析器会检查这些 ID 是否唯一。

程序清单 3-2 中的程序展示了如何解析配置文件。程序清单 3-3 中定义了配置样例。如果选择了包含字符串 - schema 的文件,那么该程序会使用 Schema 而不是 DTD。 DTD 显示在程序清单 3-4 中,很简单。

程序清单 3-5 包含了一个等价的 Schema。在这个 Schema 中,我们可以提供额外的检查: 一个 int 或 boolean 元素只能包含整数或布尔值。注意,这里使用了 xsd:group 结构来定义会 反复使用的复杂类型的各个部件。

这个例子是 XML 的典型用法。XML 格式十分健壮,足以表达复杂的关系。在此基础上,通过接管有效性检查和提供默认值等例行工作,XML 解析器添加了新的价值。

#### 程序清单 3-2 read/XMLReadTest.java

```
1 package read;
 2
  3 import java.io.*;
  4 import java.lang.reflect.*;
  5 import java.util.*;
  7 import javax.xml.parsers.*;
  9 import org.w3c.dom.*;
 import org.xml.sax.*;
 11
 12 /**
     * This program shows how to use an XML file to describe Java objects
 13
    * @version 1.0 2018-04-03
     * @author Cay Horstmann
 15
 16
    public class XMLReadTest
 18
 19
       public static void main(String[] args) throws ParserConfigurationException,
             SAXException, IOException, ReflectiveOperationException
 28
 21
          String filename:
 22
```

```
148
```

```
if (args.length == 0)
23
         {
24
            try (var in = new Scanner(System.in))
25
26
                System.out.print("Input file: ");
27
                filename = in.nextLine();
28
29
         7
30
         else
             filename = args[\theta];
32
33
         DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
34
          factory.setValidating(true);
35
36
         if (filename.contains("-schema"))
37
38
             factory.setNamespaceAware(true);
39
             final String JAXP SCHEMA LANGUAGE =
                   "http://java.sun.com/xml/jaxp/properties/schemaLanguage";
41
             final String W3C XML SCHEMA = "http://www.w3.org/2001/XMLSchema";
             factory.setAttribute(JAXP_SCHEMA_LANGUAGE, W3C_XML_SCHEMA);
43
44
45
          factory.setIgnoringElementContentWhitespace(true);
45
          DocumentBuilder builder = factory.newDocumentBuilder();
48
49
          builder.setErrorHandler(new ErrorHandler()
50
51
             {
                public void warning(SAXParseException e) throws SAXException
52
53
                {
                   System.err.println("Warning: " + e.getMessage());
54
55
56
                public void error(SAXParseException e) throws SAXException
57
58
                         System.err.println("Error: " + e.getMessage());
                         System.exit(0);
                      7
      61
                      public void fatalError(SAXParseException e) throws SAXException
      63
      64
                         System.err.println("Fatal error: " + e.getMessage());
                         System.exit(0);
      66
      67
                   });
      68
      69
      70
                Document doc = builder.parse(filename);
                Map<String, Object> config = parseConfig(doc.getDocumentElement());
      71
                System.out.println(config);
      77
      73
      74
             private static Map<String, Object> parseConfig(Element e)
      75
                   throws ReflectiveOperationException
      76
      77
```

```
var result = new HashMap<String, Object>();
78
         NodeList children = e.getChildNodes();
79
         for (int i = 0; i < children.getLength(); i++)
88
81
            var child = (Element) children.item(i);
82
            String name = child.getAttribute("id");
83
            Object value = parseObject((Element) child.getFirstChild());
84
            result.put(name, value);
85
         return result;
87
88
89
      private static Object parseObject(Element e)
QA
            throws ReflectiveOperationException
91
92
         String tagName = e.getTagName();
93
         if (tagName.equals("factory")) return parseFactory(e);
94
         else if (tagName.equals("construct")) return parseConstruct(e);
95
         else
96
97
             String childData = ((CharacterData) e.getFirstChild()).getData();
98
            if (tagName.equals("int"))
99
                return Integer.valueOf(childData);
100
             else if (tagName.equals("boolean"))
                return Boolean.valueOf(childData);
182
             else
183
                return childData:
184
         }
185
106
197
      private static Object parseFactory(Element e)
             throws ReflectiveOperationException
100
110
         String className = e.getAttribute("class");
111
         String methodName = e.getAttribute("method");
112
         Object[] args = parseArgs(e.getChildNodes()):
113
         Class<?>[] parameterTypes = getParameterTypes(args);
114
         Method method = Class.forName(className).getMethod(methodName, parameterTypes);
115
         return method.invoke(null, args);
116
117
118
119
      private static Object parseConstruct(Element e)
             throws ReflectiveOperationException
120
121
         String className = e.getAttribute("class");
123
         Object[] args = parseArgs(e.getChildNodes());
          Class<?>[] parameterTypes = getParameterTypes(args);
124
          Constructor<?> constructor = Class.forName(className).getConstructor(parameterTypes);
          return constructor.newInstance(args);
126
127
128
       private static Object[] parseArgs(NodeList elements)
129
130
             throws ReflectiveOperationException
131
          var result = new Object[elements.getLength()];
132
```

```
for (int i = 0; i < result.length; i++)
133
             result[i] = parseObject((Element) elements.item(i));
134
         return result;
135
      }
136
137
      private static Map<Class<?>, Class<?>> toPrimitive = Map.of(
138
             Integer.class, int.class,
             Boolean.class, boolean.class);
148
141
      private static Class<?>[] getParameterTypes(Object[] args)
142
143
         var result = new Class<?>[args.length];
144
          for (int i = 0; i < result.length; i++)
145
146
             Class<?> cl = args[i].getClass();
147
             result[i] = toPrimitive.get(cl);
148
             if (result[i] == null) result[i] = cl;
149
150
          return result;
151
152
153 }
```

#### 程序清单 3-3 read/config.xml

```
1 <?xml version="1.0"?>
2 <!DOCTYPE config SYSTEM "config.dtd">
3 <config>
    <entry id="background">
       <construct class="java.awt.Color">
        <int>55</int>
         <int>200</int>
         <int>100</int>
      </construct>
9
   </entry>
10
    <entry id="currency">
11
       <factory class="java.util.Currency">
12
         <string>USD</string>
13
       </factory>
14
15
     </entry>
16 </config>
```

#### 程序清单 3-4 read/config.dtd

```
1 <!ELEMENT config (entry)*>
2
3 <!ELEMENT entry (string|int|boolean|construct|factory)>
4 <!ATTLIST entry id ID #IMPLIED>
5
6 <!ELEMENT construct (string|int|boolean|construct|factory)*>
7 <!ATTLIST construct class CDATA #IMPLIED>
8
9 <!ELEMENT factory (string|int|boolean|construct|factory)*>
```

```
10 <!ATTLIST factory class CDATA #IMPLIED>
11 <!ATTLIST factory method CDATA "getInstance">
12 
13 <!ELEMENT string (#PCDATA)>
14 <!ELEMENT int (#PCDATA)>
15 <!ELEMENT boolean (#PCDATA)>
```

#### 程序清单 3-5 read/config.xsd

```
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
      <xsd:element name="config">
         <xsd:complexType>
            <xsd:sequence>
               <xsd:element name="entry" minOccurs="0" maxOccurs="unbounded">
                  <xsd:complexType>
                     <xsd:group ref="Object"/>
                     <xsd:attribute name="id" type="xsd:ID"/>
                  </xsd:complexType>
9
               </xsd:element>
10
            </xsd:sequence>
11
         </xsd:complexType>
17
      </xsd:element>
13
14
      <xsd:element name="construct">
15
         <xsd:complexType>
16
            <xsd:group ref="Arguments"/>
17
            <xsd:attribute name="class" type="xsd:string"/>
18
         </xsd:complexType>
19
      </xsd:element>
20
21
      <xsd:element name="factory">
22
23
         <xsd:complexType>
            <xsd:group ref="Arguments"/>
24
            <xsd:attribute name="class" type="xsd:string"/>
25
             <xsd:attribute name="method" type="xsd:string" default="getInstance"/>
26
27
         </xsd:complexType>
      </xsd:element>
28
29
      <xsd:group name="Object">
38
         <xsd:choice>
31
            <xsd:element ref="construct"/>
32
            <xsd:element ref="factory"/>
33
            <xsd:element name="string" type="xsd:string"/>
34
             <xsd:element name="int" type="xsd:int"/>
             <xsd:element name="boolean" type="xsd:boolean"/>
36
         </xsd:choice>
37
      </xsd:group>
38
30
40
      <xsd:group name="Arguments">
         <xsd:sequence>
41
             <xsd:group ref="Object" minOccurs="0" maxOccurs="unbounded"/>
42
         </xsd:sequence>
43
      </xsd:group>
44
  </xsd:schema>
```

# *3.5<sup>使</sup> XPath来定位信息*

*如果 定位某个XML文档中 一段 定信息 么 通过遍历DOM树 众多 点 来 査找会显得有些 烦。XPath 使得 树 点变得很容易。例如 假 有如下 HTML文档*

```
<head>
         拳 拳
      <title>. . .</title>
          攀
   </head>
</html>
```

*可以通过对XPath 式/html/head/title/text()求值来得到标 文本。 使 XPath执 下列操作比普 DOM方式 单得多*

- *1. 得文档根 点。*
- *2. 取 一个子 点 并将其 型为一个Element对 。*
- *3. 在其所有子 点中定位title<sup>元</sup> 。*
- *4. 取其 一个子元 并将其 型为一个CharacterData 点。*
- *5. 取其数据。*

*XPath可以描 XML文档中 一个 点 例如 下面的XPath*

*/html/body/form*

*描 了 XHTML文件中body元素的子元 中所有 form元 。可以 [】操作 来 择 定 元*

*/html/body/form[l]*

*<sup>是</sup> 一个form ( 引号从1开始)。*

*使 @操作 可以得到属性值。XPath 式*

*/html/body/fonn[l]/@action*

*描 了 一个 中 action属性。XPath表达式*

*/htnl/body/fom/@dction*

*描 了 body元 子元 中所有form元素的所有action属性 点。*

*XPath有很多有 函数 例如*

*count(/html/body/form)*

*回body元 forw子元 数 。 XPath 式 有很多 参 http://www.w3c. org/TR/xpath 或 在 http://www.zvon.org/xxl/XPathTutorial/General/examples.html 上 一个 常好 在 指南。*

*要计算XPath 式 先需要从XPathFactory创建一个XPath对*

XPathFactory xpfactory = XPathFactory.newInstance();
path = xpfactory.newXPath();

然后, 调用 evaluate 方法来计算 XPath 表达式:

String username = path.evaluate("/html/head/title/text()", doc);

可以用同一个 XPath 对象来计算多个表达式。

这种形式的 evaluate 方法将返回一个字符串。这很适合用来获取文本,比如前面的例子中的 title 元素的文本子节点。如果 XPath 表达式产生了一组节点,请做如下调用:

XPathNodes result = path.evaluateExpression("/html/body/form", doc, XPathNodes.class);

XPathNodes 类与 NodeList 类相似,但是它扩展了 Iterable 接口,使得我们可以使用增强型 for 循环。

这个方法是在 Java 9 中添加进来的, 在老版本中, 需要使用下面这条语句:

var nodes = (NodeList) path.evaluate("/html/body/form", doc, XPathConstants.NODESET);

如果结果只有一个节点,则使用下面的调用:

Node node = path.evaluateExpression("/html/body/form[1]", doc, Node.class); node = (Node) path.evaluate("/html/body/form[1]", doc, XPathConstants.NODE);

如果结果是一个数字,则使用:

int count = path.evaluateExpression("count(/html/body/form)", doc, Integer.class);
count = ((Number) path.evaluate("count(/html/body/form)",

不必从文档的根节点开始搜索,可以从任意一个节点或节点列表开始。例如,如果有前 一次计算得到的节点,那么就可以调用:

String result = path.evaluate(expression, node);

如果不知道 XPath 表达式的计算结果是什么(可能该表达式来自于用户), 那么就调用 XPathEvaluationResult<?> result = path.evaluateExpression(expression, doc);

表达式 result.type() 是下列 XPathEvaluationResult.XPathResultType 枚举常量之一:

STRING

NODESET

NODE

NUMBER

**BOOLEAN** 

调用 result.value() 可以获取结果值。

程序清单 3-6 展示了对任意的 XPath 表达式的计算过程。加载一个 XML 文件,输入一个表达式,该表达式的结果就会显示出来。

#### 程序清单 3-6 xpath/XPathTest.java

```
package xpath;
```

2

3 import java.io.\*;

```
4 import java.nio.file.*;
5 import java.util.*;
   import javax.xml.catalog.*;
   import javax.xml.parsers.*;
   import javax.xml.xpath.*;
10
  import org.w3c.dom.*;
   import org.xml.sax.*;
13
14
   * This program evaluates XPath expressions.
    * @version 1.1 2018-04-06
16
    * @author Cay Horstmann
17
   */
18
  public class XPathTest
19
28
      public static void main(String[] args) throws Exception
22
         DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
23
         DocumentBuilder builder = factory.newDocumentBuilder();
25
         // Avoid a delay in parsing an XHTML file--see the first note in
26
         // Section 3.3.1
27
         builder.setEntityResolver(CatalogManager.catalogResolver(
28
                CatalogFeatures.defaults(),
               Paths.get("xpath/catalog.xml").toAbsolutePath().toUri()));
30
31
         XPathFactory xpfactory = XPathFactory.newInstance();
32
         XPath path = xpfactory.newXPath();
33
         try (var in = new Scanner(System.in))
34
             String filename;
            if (args.length == 0)
37
38
                System.out.print("Input file: ");
39
                filename = in.nextLine();
48
             }
41
             else
                filename = args[\theta];
43
44
             Document doc = builder.parse(filename);
             var done = false;
46
             while (!done)
47
48
                System.out.print("XPath expression (empty line to exit): " );
49
                String expression = in.nextLine():
50
                if (expression.trim().isEmpty()) done = true;
51
                else
52
53
                {
                   try
55
                      XPathEvaluationResult<?> result
56
                            = path.evaluateExpression(expression, doc);
57
```

```
if (result.type() == XPathEvaluationResult.XPathResultType.NODESET)
58
59
                         for (Node n : (XPathNodes) result.value())
68
                            System.out.println(description(n));
61
                      }
62
                      else if (result.type() == XPathEvaluationResult.XPathResultType.NODESET)
63
                         System.out.println((Node) result.value());
64
65
                         System.out.println(result.value());
66
67
                   catch (XPathExpressionException e)
68
69
                      System.out.println(e.getMessage());
70
71
72
            }
73
         }
74
      }
75
76
      public static String description(Node n)
77
78
         if (n instanceof Element) return "Element " + n.getNodeName();
79
         else if (n instanceof Attr) return "Attribute " + n;
88
          else return n.toString();
81
82
83 }
```

#### API javax.xml.xpath.XPathFactory 5.0

- static XPathFactory newInstance() 返回用于创建 XPath 对象的 XPathFactory 实例。
- XPath newXpath() 构建用于计算 XPath 表达式的 XPath 对象。

# API javax.xml.xpath.XPath 5.0

- String evaluate(String expression, Object startingPoint) 从给定的起点计算表达式。起点可以是一个节点或节点列表。如果结果是一个节点或 节点集、则返回的字符串由所有文本节点子元素的数据构成。
- Object evaluate(String expression, Object startingPoint, OName resultType) 从给定的起点计算表达式。起点可以是一个节点或节点列表。resultType 是 XPath-Constants 类的常量 STRING、NODE、NODESET、NUMBER 或 BOOLEAN 之一。返回值是 String、 Node、NodeList、Number 或 Boolean。
- <T> T evaluateExpression(String expression, Object item, Class<T> type) 计算给定表达式,并产生给定类型值的结果。
- XPathEvaluationResult<?> evaluateExpression(String expression, InputSource source) 计算给定表达式。

## API javax.xml.xpath.XPathEvaluationResult<T> 9

- XPathEvaluationResult.XPathResultType type()
   返回枚举常量 STRING、NODESET、NODE、NUMBER 和 BOOLEAN 之一。
- T value()返回结果值。

# 3.6 使用命名空间

Java 语言使用包来避免名字冲突。程序员可以为不同的类使用相同的名字,只要它们不在同一个包中即可。XML 也有类似的命名空间(namespace)机制,可以用于元素名和属性名。

名字空间是由统一资源标识符 (Uniform Resource Identifier, URI) 来标识的, 比如:

http://www.w3.org/2001/XMLSchema

uuid:1c759aed-b748-475c-ab68-10679700c4f2

urn:com:books-r-us

HTTP 的 URL 格式是最常见的标识符。注意, URL 只用作标识符字符串, 而不是一个文件的定位符。例如, 名字空间标识符:

http://www.horstmann.com/corejava

http://www.horstmann.com/corejava/index.html

表示了不同的命名空间,尽管 Web 服务器将为这两个 URL 提供同一个文档。

在命名空间的 URL 所表示的位置上不需要有任何文档, XML 解析器不会尝试去该处查找任何东西。然而,为了给可能会遇到不熟悉的命名空间的程序员提供一些帮助,人们习惯于将用于解释该命名空间的文档放在 URL 位置上。例如,如果把浏览器指向 XML Schema的命名空间 URL (http://www.w3.org/2001/XMLSchema),就会发现一个描述 XML Schema 标准的文档。

为什么要用 HTTP URL 作为命名空间的标识符?这是因为这样容易确保它们是独一无二的。如果使用实际的 URL,那么主机部分的唯一性就将由域名系统来保证。然后,你的组织可以安排 URL 余下部分的唯一性,这和 Java 包名中的反向域名是一个原理。

尽管长名字空间的唯一性很好,但是你肯定不想处理超出必需范围的长标识符。在 Java 编程语言中,可以用 import 机制来指定很长的包名,然后就可以只使用较短的类名了。在 XML 中有类似的机制、比如:

<element xmlns="namespaceURI">
 children
</element>

现在,该元素和它的子元素都是给定命名空间的一部分了。 子元素可以提供自己的命名空间,例如: <element xmlns="namespaceURI1">
 <child xmlns="namespaceURI2">
 grandchildren
 </child>
 more children
</element>

这时,第一个子元素和孙元素都是第二个命名空间的一部分。

无论是只需要一个命名空间,还是命名空间本质上是嵌套的,这个简单机制都工作得很好。如若不然,就需要使用第二种机制,而 Java 中并没有类似的机制。你可以用一个前缀来表示命名空间,即为特定文档选取的一个短的标识符。下面是一个典型的例子:

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
 <xsd:element name="config"/>

</xsd:schema>

下面的属性:

xmlns:prefix="namespaceURI"

用于定义命名空间和前缀。在我们的例子中,前缀是字符串 xsd。这样, xsd:schema 实际上指的是命名空间 http://www.w3.org/2001/XMLSchema 中的 schema。

直 注释: 只有子元素继承了它们父元素的命名空间,而不带显式前缀的属性并不是命名空间的一部分。请看下面这个特意构造出来的例子:

<configuration xmlns="http://www.horstmann.com/corejava"
xmlns:si="http://www.bipm.fr/enus/3\_SI/si.html">
 <size value="210" si:unit="mm"/>

</configuration>

在这个示例中,元素 configuration 和 size 是 URI 为 http://www.horstmann.com/ corejava 的命名空间的一部分。属性 si:unit 是 URI 为 http://www.bipm.fr/enus/3\_SI/si.html 的命名空间的一部分。然而,属性 value 不是任何命名空间的一部分。

可以控制解析器对命名空间的处理。默认情况下, Java XML 库的 DOM 解析器并非"命名空间感知的"。

要打开命名空间处理特性, 请调用 DocumentBuilderFactory 类的 setNamespace Aware 方法:

DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance(); factory.setNamespaceAware(true);

这样, 该工厂产生的所有生成器便都支持命名空间了。

或者, 从 Java 13 开始, 可以调用:

DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();

生成器创建的每个节点都有三个属性:

• 带有前缀的限定名 (qualified name),由 getNodeName 和 getTagName 等方法返回。

- 命名空间 URI, 由 getNamespaceURI 方法返回。
- 不带前缀和命名空间的本地名 (local name),由 getLocalName 方法返回。

下面是一个例子。假设解析器看到了以下元素:

<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">

它会报告如下信息:

- 限定名 = xsd:schema
- 命名空间 URI = http://www.w3.org/2001/XMLSchema
- 本地名 = schema
- **注释**:如果对命名空间的感知特性被关闭,getLocalName 和 getNamespaceURI 方法将返回 null。

#### API org.w3c.dom.Node

- String getLocalName()
   返回本地名(不带前缀),或者在解析器不感知命名空间时,返回 null。
- String getNamespaceURI()
   返回命名空间 URI,或者在解析器不感知命名空间时,返回 null。

#### API javax.xml.parsers.DocumentBuilderFactory

- static DocumentBuilderFactory newNSInstance() 13
   产生一个工厂,它创建的生成器都是命名空间感知的。
- boolean isNamespaceAware()
- void setNamespaceAware(boolean value)
   获取或设置工厂的 namespaceAware 属性。当设为 true 时,工厂产生的解析器是命名空间感知的。

# 3.7 流机制解析器

DOM 解析器会完整地读入 XML 文档,然后将其转换成一个树形的数据结构。对于大多数应用,DOM 都运行得很好。但是,如果文档很大,并且处理算法又非常简单,可以在运行时解析节点,而不必看到完整的树形结构,那么 DOM 可能就会显得效率低下了。在这种情况下,我们应该使用流机制解析器 (streaming parser)。

在下面的小节中,我们将讨论 Java 类库提供的流机制解析器:老而弥坚的 SAX 解析器和添加到 Java 6 中的更现代化的 StAX 解析器。SAX 解析器使用的是事件回调(event callback),而 StAX 解析器提供了遍历解析事件的迭代器,后者用起来通常更方便一些。

#### 3.7.1 使用 SAX 解析器

SAX 解析器在解析 XML 输入数据的各个组成部分时会报告事件,但不会以任何方式存储文档,而是交由事件处理器构建相应的数据结构。实际上,DOM 解析器是在 SAX 解析器

的基础上构建的,它在接收到解析器事件时构建 DOM 树。

在使用 SAX 解析器时,需要一个处理器来为各种解析器事件定义事件动作。Content-Handler 接口定义了若干个在解析文档时解析器会调用的回调方法。下面是最重要的几个:

- startElement 和 endElement 在每当遇到起始或终止标签时调用。
- characters 在每当遇到字符数据时调用。
- startDocument 和 endDocument 分别在文档开始和结束时各调用一次。

例如,在解析以下片段时:

<font>
 <name>Helvetica</name>
 <size units="pt">36</size>
</font>

#### 解析器会产生以下回调:

- 1. startElement, 元素名: font
- 2. startElement, 元素名: name
- 3. characters. 内容: Helvetica
- 4. endElement, 元素名: name
- 5. startElement, 元素名: size, 属性: units="pt"
- 6. characters, 内容: 36
- 7. endElement, 元素名: size
- 8. endElement, 元素名: font

处理器必须覆盖这些方法,让它们执行在解析文件时我们想要让它们执行的动作。本节最后的程序会打印出一个 HTML 文件中的所有链接 <a href="...">。它直接覆盖了处理器的 startElement 方法,以检查名字为 a,且属性名为 href 的链接,其潜在用途包括用于实现"网络爬虫",即一个沿着链接到达越来越多网页的程序。

註釋: 遗憾的是,HTML不必是合法的XML,大多数HTML页面都与良构的XML差别很大,以至于示例程序无法解析它们。但是,W3C编写的大部分页面都是用XHTML编写的,XHTML是一种HTML方言,且是良构的XML,你可以用这些页面来测试示例程序。例如,运行:

java SAXTest http://www.w3c.org/Consortium

将看到由那个页面上所有链接的URL构成的列表。

示例程序是一个很好的使用 SAX 的例子。我们根本不在乎 a 元素出现的上下文环境,而且不必存储树形结构。

下面是如何得到 SAX 解析器的代码:

SAXParserFactory factory = SAXParserFactory.newInstance();
SAXParser parser = factory.newSAXParser();

现在可以处理文档了:

parser.parse(source, handler);

这里的 source 可以是一个文件、一个 URL 字符串或者是一个输入流。handler 属于 Default-Handler 的某个子类,DefaultHandler 类为以下四个接口定义了空的方法:

ContentHandler DTDHandler EntityResolver ErrorHandler

示例程序定义了一个处理器,它覆盖了 ContentHandler 接口的 startElement 方法,以观察带有 href 属性的 a 元素。

```
var handler = new DefaultHandler()
{
    public void startElement(String namespaceURI, String lname, String qname,
```

startElement 方法有 3 个描述元素名的参数,其中 qname 参数以 prefix:localname 的形式报告限定名。如果命名空间处理特性已经打开,那么 namespaceURI 和 lname 参数提供的就是命名空间和本地(非限定)名。

与 DOM 解析器一样,命名空间处理特性默认是关闭的,可以调用工厂类的 setNames-paceAware 方法来激活命名空间处理特性,或者从 Java 13 开始,用 newNSInstance 来创建命名空间感知的工厂:

```
SAXParserFactory factory = SAXParserFactory.newNSInstance();
SAXParser saxParser = factory.newSAXParser();
```

在这个程序中,我们还处理了另一个常见的问题。XHTML 文件总是以一个包含对 DTD 引用的标签开头,解析器会加载这个 DTD。可以理解的是,W3C 肯定不乐意对诸如 www. w3.org/TR/xhtml/DTD/xhtml-strict.dtd 这样的文件提供千万亿次的下载。总有一天他们会完全拒绝提供这些文件,但到写本章时为止,他们还在并不情愿地提供 DTD 下载。如果你不需要验证文件,只需调用:

factory.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);

程序清单 3-7 包含了网络爬虫程序的代码。在本章的后续部分,将会看到 SAX 的另一个有趣用法,即将非 XML 数据源转换成 XML 的一种简单方式是报告 XML 解析器报告的 SAX 事件。详情请参见 3.9 节。

#### 程序清单 3-7 sax/SAXTest.java

```
1 package sax;
2
3 import java.io.*;
4 import java.net.*;
5 import javax.xml.parsers.*;
6 import org.xml.sax.*;
   import org.xml.sax.helpers.*;
   /**
9
    * This program demonstrates how to use a SAX parser. The program prints all
10
    * hyperlinks of an XHTML web page. <br>
11
    * Usage: java sax.SAXTest URL
12
    * @version 1.01 2018-05-01
    * @author Cay Horstmann
14
15
   public class SAXTest
16
17
      public static void main(String[] args) throws Exception
18
19
         String url;
28
         if (args.length == 0)
21
22
            url = "http://www.w3c.org";
23
             System.out.println("Using " + url);
24
25
         else url = args[0];
26
         var handler = new DefaultHandler()
28
29
             {
                public void startElement(String namespaceURI, String lname,
30
                      String gname, Attributes attrs)
31
32
                   if (lname.equals("a") && attrs != null)
33
34
                      for (int i = 0; i < attrs.getLength(); i++)
35
36
                         String aname = attrs.getLocalName(i);
37
38
                         if (aname.equals("href"))
                            System.out.println(attrs.getValue(i));
39
4B
                   }
41
                }
42
             };
43
44
          SAXParserFactory factory = SAXParserFactory.newInstance();
45
          factory.setNamespaceAware(true);
46
          factory.setFeature(
47
             "http://apache.org/xml/features/nonvalidating/load-external-dtd",
48
49
          SAXParser saxParser = factory.newSAXParser();
50
          InputStream in = new URL(url).openStream();
51
          saxParser.parse(in, handler);
52
53
   }
54
```

#### API javax.xml.parsers.SAXParserFactory

- static SAXParserFactory newInstance()
- static SAXParserFactory newNSInstance() 13
   返回 SAXParserFactory 类的一个实例。第二种方法产生一个命名空间感知的实例。
- SAXParser newSAXParser()
   返回 SAXParser 类的一个实例。
- boolean isNamespaceAware()
- void setNamespaceAware(boolean value)
   获取和设置工厂的 namespaceAware 属性。当设为 true 时,该工厂生成的解析器是命名空间感知的。
- boolean isValidating()
- void setValidating(boolean value)
   获取和设置工厂的 validating 属性。当设为 true 时,该工厂生成的解析器将要验证其输入。

#### API javax.xml.parsers.SAXParser

- void parse(File f, DefaultHandler handler)
- void parse(String url, DefaultHandler handler)
- void parse(InputStream in, DefaultHandler handler)
   解析来自给定文件、URL 或输入流的 XML 文档,并把解析事件报告给指定的处理器。

# API org.xml.sax.ContentHandler

- void startDocument()
- void endDocument()
   在文档的开头和结尾处被调用。
- void startElement(String uri, String lname, String qname, Attributes attr)
- void endElement(String uri, String lname, String qname)
   在元素的开头和结尾处被调用。如果解析器是名字空间感知的,那么它会报告名字空间的 URI、无前缀的本地名字,以及带前缀的限定名。
- void characters(char[] data, int start, int length)
   解析器报告字符数据时被调用。

# API org.xml.sax.Attributes

- int getLength() 返回存储在该属性集合中的属性数量。
- String getLocalName(int index)

返回给定索引的属性的本地名(无前缀),或在解析器不是命名空间感知的情况下返回 空字符串。

- String getURI(int index)
  - 返回给定索引的属性的命名空间 URI,或者,当该节点不是命名空间的一部分.或解 析器并非命名空间感知时返回空字符串。
- String getQName(int index) 返回给定索引的属性的限定名(带前缀),或当解析器不报告限定名时返回空字符串。
- String getValue(int index)
- String getValue(String gname)
- String getValue(String uri, String lname) 根据给定索引、限定名或命名空间 URI+ 本地名来返回属性值; 当该值不存在时, 返 III nulla

#### 3.7.2 使用 StAX 解析器

StAX 解析器是一种"拉解析器"(pull parser),与安装事件处理器不同,你只需使用下面 这样的基础循环来迭代所有的事件:

```
InputStream in = url.openStream();
XMLInputFactory factory = XMLInputFactory.newInstance();
XMLStreamReader parser = factory.createXMLStreamReader(in);
while (parser.hasNext())
{
   int event = parser.next();
   Call parser methods to obtain event details
例如,在解析下面的片段时
<font>
   <name>Helvetica</name>
   <size units="pt">36</size>
</font>
解析器将产生下面的事件:
```

- 1. START ELEMENT, 元素名: font
- 2. CHARACTERS,内容:空白字符
- 3. START ELEMENT, 元素名: name
- 4. CHARACTERS, 内容: Helvetica
- 5. END ELEMENT, 元素名: name
- 6. CHARACTERS,内容:空白字符
- 7. START ELEMENT, 元素名: size
- 8. CHARACTERS, 内容: 36
- 9. END ELEMENT, 元素名: size

- 10. CHARACTERS, 内容: 空白字符
- 11. END ELEMENT, 元素名: font

要分析这些属性值,需要调用 XMLStreamReader 类中恰当的方法,例如:

String units = parser.getAttributeValue(null, "units");

它可以获取当前元素的 units 属性。

默认情况下,命名空间处理是启用的,可以通过像下面这样修改工厂来使其无效:

```
XMLInputFactory factory = XMLInputFactory.newInstance();
factory.setProperty(XMLInputFactory.IS NAMESPACE AWARE, false);
```

程序清单 3-8 包含了用 StAX 解析器实现的网络爬虫程序。正如你所见,这段代码比等 效的 SAX 代码要简短了许多,因为此时我们不必操心事件处理问题。

#### 程序清单 3-8 stax/StAXTest.java

```
package stax;
2
3 import java.io.*;
   import java.net.*;
5 import javax.xml.stream.*;
   /**
7
   * This program demonstrates how to use a StAX parser. The program prints all
   * hyperlinks links of an XHTML web page. <br>
    * Usage: java stax.StAXTest URL
   * @author Cay Horstmann
11
   * @version 1.1 2018-05-01
13
  public class StAXTest
14
      public static void main(String[] args) throws Exception
16
      {
17
         String urlString;
         if (args.length == 0)
19
20
            urlString = "http://www.w3c.org";
21
            System.out.println("Using " + urlString);
22
23
         else urlString = args[θ];
24
         var url = new URL(urlString);
25
         InputStream in = url.openStream();
26
         XMLInputFactory factory = XMLInputFactory.newInstance();
27
         XMLStreamReader parser = factory.createXMLStreamReader(in);
28
         while (parser.hasNext())
29
30
            int event = parser.next();
31
            if (event == XMLStreamConstants.START ELEMENT)
32
33
               if (parser.getLocalName().equals("a"))
34
                   String href = parser.getAttributeValue(null, "href");
36
                   if (href != null)
37
```

```
System.out.println(href);
38
39
             }
          }
41
       }
42
43 }
```

#### API javax.xml.stream.XMLInputFactory

- static XMLInputFactory newInstance() 返回 XMLInputFactory 类的一个实例。
- void setProperty(String name, Object value)

设置这个工厂的属性,或者在要设置的属性不支持设置成给定值时,抛出 Illegal-Argument Exception。JDK 的实现支持下列 Boolean 类型的属性:

"javax.xml.stream.isValidating"

为 false (默认值) 时, 不验证文档 (规范

不要求必须支持)。

"javax.xml.stream.isNamespaceAware"

为 true (默认值) 时, 将处理命名空间 (规

范不要求必须支持)。

"javax.xml.stream.isCoalescing"

为 false (默认值) 时, 邻近的字符数据不

进行连接。

"javax.xml.stream.isReplacingEntityReferences"为true(默认值)时,实体引用将作为字符

数据被替换和报告。

"javax.xml.stream.isSupportingExternalEntities" 为 true(默认值)时,外部实体将被解析。

规范对于这个属性没有给出默认值。

"javax.xml.stream.supportDTD"

为 true (默认值) 时, DTD 将作为事件被报告。

- XMLStreamReader createXMLStreamReader(InputStream in)
- XMLStreamReader createXMLStreamReader(InputStream in, String characterEncoding)
- XMLStreamReader createXMLStreamReader(Reader in)
- XMLStreamReader createXMLStreamReader(Source in) 创建一个从给定的流、阅读器或 JAXP 源读人的解析器。

# API javax.xml.stream.XMLStreamReader

- boolean hasNext() 如果有另一个解析事件,则返回 true。
- int next()

将解析器的状态设置为下一个解析事件,并返回下列常量之一: START ELEMENT、END ELEMENT、CHARACTERS、START DOCUMENT、END DOCUMENT、CDATA、COMMENT、SPACE(可忽略 的空白字符)、PROCESSING INSTRUCTION、ENTITY REFERENCE、DTD。

- 166
  - boolean isStartElement()
  - boolean isEndElement()
  - boolean isCharacters()
  - boolean isWhiteSpace()如果当前事件是一个开始元素、结束元素、字符数据或空白字符,则返回 true。
  - QName getName()
  - String getLocalName()
     获取在 START ELEMENT 或 END ELEMENT 事件中的元素的名字。
  - 获取在 START\_ELEMENT 或 END\_ELEMENT 事件中的元素的名字。● String getText()
    - 返回一个 CHARACTERS、COMMENT 或 CDATA 事件中的字符,或一个 ENTITY\_REFERENCE 的替换值,或者一个 DTD 的内部子集。
  - int getAttributeCount()
  - QName getAttributeName(int index)
  - String getAttributeLocalName(int index)
  - String getAttributeValue(int index)
     如果当前事件是 START\_ELEMENT,则获取属性数量和属性的名字与值。
  - String getAttributeValue(String namespaceURI, String name)
     如果当前事件是 START\_ELEMENT,则获取具有给定名称的属性的值。如果 namespaceURI 为 null,则不检查名字空间。

# 3.8 生成 XML 文档

现在你已经知道怎样编写读取 XML 的 Java 程序了。下面让我们开始介绍它的反向过程,即产生 XML 输出。当然,你可以直接通过一系列 print 调用,打印出各元素、属性和文本内容,以此来编写 XML 文件,但这并不是一个好主意。这样的代码会非常冗长复杂,对于属性值和文本内容中的那些特殊符号(如 "和 <),一不注意就会出错。

一种更好的方式是用文档的内容构建一棵 DOM 树,然后再写出该树的所有内容。下面的小节将讨论其细节。

# 3.8.1 不带命名空间的文档

要建立一棵 DOM 树,可以从一个空的文档开始。通过调用 Document Builder 类的 new Document 方法可以得到一个空文档。

Document doc = builder.newDocument();

使用 Document 类的 createElement 方法可以构建文档里的元素:

Element rootElement = doc.createElement(rootName);
Element childElement = doc.createElement(childName);

使用 createTextNode 方法可以构建文本节点:

Text textNode = doc.createTextNode(textContents);

使用以下方法可以给文档添加根元素,给父结点添加子节点:

doc.appendChild(rootElement);
rootElement.appendChild(childElement);
childElement.appendChild(textNode);

在建立 DOM 树时,可能还需要设置元素属性,这只需调用 Element 类的 setAttribute 方法即可:

rootElement.setAttribute(name, value);

#### 3.8.2 带命名空间的文档

如果要使用命名空间,那么创建文档的过程就会稍微有些差异。

首先需要将生成器工厂设置为是命名空间感知的,然后创建生成器:

DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
factory.setNamespaceAware(true);
builder = factory.newDocumentBuilder();

再使用 createElementNS 而不是 createElement 来创建所有节点:

String namespace = "http://www.w3.org/2000/svg"; Element rootElement = doc.createElementNS(namespace, "svg");

如果节点具有带命名空间前缀的限定名,那么所有必需的带有 xmlns 前缀的属性都会被自动创建。例如,如果需要在 HTML 中包含 SVG,那么就可以像下面这样构建元素:

Element svgElement = doc.createElement(namespace, "svg:svg")

当该元素被写人 XML 文件时, 它会转变为:

<svg:svg xmlns:svg="http://www.w3.org/2000/svg">

如果需要设置的元素属性的名字位于命名空间中,那么可以使用 Element 类的 setAttributeNS 方法:

rootElement.setAttributeNS(namespace, qualifiedName, value);

# 3.8.3 写出文档

有些奇怪的是,把 DOM 树写出到输出流中并非一件易事。最容易的方式是使用可扩展的样式表语言转换(Extensible Stylesheet Language Transformations, XSLT) API。关于 XSLT 的更多信息请参见 3.9 节。当下,我们先考虑根据生成 XML 输出的"魔咒"而编写的代码。

我们把"不做任何操作"的转换应用于文档,并且捕获它的输出。为了将 DOCTYPE 节点 纳入输出,我们还需要将 SYSTEM 和 PUBLIC 标识符设置为输出属性。

```
// construct the do-nothing transformation
Transformer t = TransformerFactory.newInstance().newTransformer();
// set output properties to get a DOCTYPE node
t.setOutputProperty(OutputKeys.DOCTYPE SYSTEM, systemIdentifier);
```

```
t.setOutputProperty(OutputKeys.DOCTYPE PUBLIC, publicIdentifier);
// set indentation
t.setOutputProperty(OutputKeys.INDENT, "yes");
t.setOutputProperty(OutputKeys.METHOD, "xml");
t.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
// apply the do-nothing transformation and send the output to a file
t.transform(new DOMSource(doc), new StreamResult(new FileOutputStream(file)));
另一种方式是使用 LSSerializer 接口。为了获取实例,可以使用下面的魔咒:
DOMImplementation impl = doc.getImplementation();
var implLS = (DOMImplementationLS) impl.getFeature("LS", "3.0");
LSSerializer ser = implLS.createLSSerializer();
如果需要空格和换行,可以设置下面的标志:
ser.getDomConfig().setParameter("format-pretty-print", true);
然后可以易如反掌地将文档转换为字符串:
String str = ser.writeToString(doc);
如果想要将输出直接写入到文件中,则需要一个 LSOutput:
LSOutput out = implLS.createLSOutput();
out.setEncoding("UTF-8");
out.setByteStream(Files.newOutputStream(path));
ser.write(doc, out);
```

#### api javax.xml.parsers.DocumentBuilder

Document newDocument()
 返回一个空文档。

#### API org.w3c.dom.Document 1.4

- Element createElement(String name)
- Element createElementNS(String uri, String qname) 返回具有给定名字的元素。
- Text createTextNode(String data)
   返回具有给定数据的文本节点。

#### API org.w3c.dom.Node

Node appendChild(Node child)
 在该节点的子节点列表中追加一个节点。返回被追加的节点。

#### API org.w3c.dom.Element 1.4

- void setAttribute(String name, String value)
- void setAttributeNS(String uri, String qname, String value)
   将有给定名字的属性设置为指定的值。
   如果限定名有别名前缀,则 uri 不能为 null。

#### API javax.xml.transform.TransformerFactory

- static TransformerFactory newInstance()
   返回 TransformerFactory 类的一个实例。
- Transformer newTransformer()
   返回 Transformer 类的一个实例,它实现了标识符转换(不做任何事情的转换)。

#### API javax.xml.transform.Transformer

void setOutputProperty(String name, String value)

设置输出属性。标准输出属性参见 http://www.w3.org/TR/xslt#output, 其中最有用的几个如下所示:

doctype-public DOCTYPE声明中使用的公共 ID

doctype-system DOCTYPE 声明中使用的系统 ID

Indent

"ves"或者 "no"

method

"xml" "html" "text" 或定制的字符串

void transform(Source from, Result to)
 转换一个 XML 文档。

#### API javax.xml.transform.dom.DOMSource

DOMSource(Node n)
 从给定的节点中构建一个源。通常,n是文档节点。

# API javax.xml.transform.stream.StreamResult 1.4

- StreamResult(File f)
- StreamResult(OutputStream out)
- StreamResult(Writer out)
- StreamResult(String systemID)
   从文件、流、写出器或系统 ID (通常是相对或绝对 URL) 中构建流结果。

## 3.8.4 使用 StAX 写出 XML 文档

在前一节中,你看到了如何通过写出 DOM 树的方法来产生 XML 文件。如果这个 DOM 树没有其他任何用途,那么这种方式就不是很高效。

StAX API 使我们可以直接将 XML 树写出,这需要从某个 OutputStream 中构建一个 XML-StreamWriter,就像下面这样:

XMLOutputFactory factory = XMLOutputFactory.newInstance(); XMLStreamWriter writer = factory.createXMLStreamWriter(out);

要产生 XML 文件头,需要调用

writer.writeStartDocument()

#### 然后调用

writer.writeStartElement(name);

#### 添加属性需要调用

writer.writeAttribute(name, value);

现在,可以通过再次调用 writeStartElement 添加新的子节点,或者用下面的调用写出字符: writer.writeCharacters(text);

在写完所有子节点之后, 调用

writer.writeEndElement();

#### 这会导致当前元素被关闭。

要写出没有子节点的元素 (例如 <img .../>), 可以使用下面的调用

writer.writeEmptyElement(name);

最后,在文档的结尾,调用

writer.writeEndDocument();

#### 关闭所有打开的元素。

你仍旧需要关闭 XMLStreamWriter,并且需要人为关闭它,因为 XMLStreamWriter 接口没有扩展 AutoCloseable 接口。

与使用 DOM/XSLT 的方式一样,我们不必担心属性值和字符数据中的转义字符。但是,我们仍旧有可能会产生非良构的 XML,例如具有多个根节点的文档。并且,StAX 当前的版本还没有任何对产生缩进输出的支持。

程序清单 3-9 中的程序展示了写出 XML 的两种方式。

#### 程序清单 3-9 write/XMLWriteTest.java

```
1 package write;
3 import java.io.*;
4 import java.nio.file.*;
5 import java.util.*;
7 import javax.xml.parsers.*;
8 import javax.xml.stream.*;
9 import javax.xml.transform.*;
import javax.xml.transform.dom.*;
import javax.xml.transform.stream.*;
12
13 import org.w3c.dom.*;
14
15 /**
* This program shows how to write an XML file. It produces modern art in SVG
   * @version 1.13 2021-09-03
   * @author Cay Horstmann
28
```

```
public class XMLWriteTest
   {
22
      public static void main(String[] args) throws Exception
23
24
         Document doc = newDrawing(600, 400);
25
         writeDocument(doc, "drawing1.svg");
26
         writeNewDrawing(600, 400, "drawing2.svg");
27
28
29
      private static Random generator = new Random();
38
31
37
       * Creates a new random drawing.
33
       * @param drawingWidth the width of the drawing in pixels
34
       * @param drawingHeight the width of the drawing in pixels
35
       * @return the DOM tree of the SVG document
36
37
      public static Document newDrawing(int drawingWidth, int drawingHeight)
38
            throws ParserConfigurationException
39
48
         DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
41
         factory.setNamespaceAware(true);
47
         DocumentBuilder builder = factory.newDocumentBuilder();;
43
         String namespace = "http://www.w3.org/2000/svg";
         Document doc = builder.newDocument();
45
         Element svgElement = doc.createElementNS(namespace, "svg");
46
         doc.appendChild(svgElement);
47
         svgElement.setAttribute("width", "" + drawingWidth);
48
         svgElement.setAttribute("height", "" + drawingHeight);
49
         int n = 10 + generator.nextInt(20);
58
         for (int i = 1; i <= n; i++)
51
52
             int x = generator.nextInt(drawingWidth);
53
            int y = generator.nextInt(drawingHeight);
54
            int width = generator.nextInt(drawingWidth - x);
55
            int height = generator.nextInt(drawingHeight - y);
56
            int r = generator.nextInt(256);
57
            int g = generator.nextInt(256);
58
            int b = generator.nextInt(256);
59
6A
             Element rectElement = doc.createElementNS(namespace, "rect");
61
             rectElement.setAttribute("x", "" + x);
             rectElement.setAttribute("y", "" + y);
63
             rectElement.setAttribute("width", "" + width);
            rectElement.setAttribute("height", "" + height);
65
             rectElement.setAttribute("fill",
66
                "#%02x%02x%02x".formatted(r, g, b));
             svgElement.appendChild(rectElement);
68
69
70
          return doc;
71
72
73
       * Saves a document using DOM/XSLT.
74
```

```
* @param doc the document to be written
75
       * @param filename the name of the destination file
76
77
      public static void writeDocument(Document doc, String filename)
78
            throws TransformerException, IOException
79
88
         Transformer t = TransformerFactory.newInstance().newTransformer();
         t.setOutputProperty(OutputKeys.DOCTYPE SYSTEM,
82
               "http://www.w3.org/TR/2000/CR-SVG-20000802/DTD/svg-20000802.dtd");
83
         t.setOutputProperty(OutputKeys.DOCTYPE PUBLIC,
                "-//W3C//DTD SVG 20000802//EN");
85
         t.setOutputProperty(OutputKeys.INDENT, "yes");
         t.setOutputProperty(OutputKeys.METHOD, "xml");
87
         t.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
88
         t.transform(new DOMSource(doc), new StreamResult(
               Files.newOutputStream(Path.of(filename))));
91
92
      /**
93
       * Uses StAX to write an SVG document with a random drawing.
       * @param drawingWidth the width of the drawing in pixels
95
96
       * @param drawingHeight the width of the drawing in pixels
       * @param filename the name of the destination file
98
      public static void writeNewDrawing(int drawingWidth, int drawingHeight,
99
            String filename) throws XMLStreamException, IOException
100
101
         XMLOutputFactory factory = XMLOutputFactory.newInstance();
182
         XMLStreamWriter writer = factory.createXMLStreamWriter(
103
                Files.newOutputStream(Path.of(filename)));
184
         writer.writeStartDocument();
185
         writer.writeDTD("""
186
      <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20000802//EN"
187
         "http://www.w3.org/TR/2000/CR-SVG-20000802/DTD/svg-20000802.dtd">
188
      """);
109
         writer.writeStartElement("svg");
118
         writer.writeDefaultNamespace("http://www.w3.org/2000/svg");
111
         writer.writeAttribute("width", "" + drawingWidth);
112
         writer.writeAttribute("height", "" + drawingHeight);
113
         int n = 10 + generator.nextInt(20);
114
         for (int i = 1; i <= n; i++)
115
116
             int x = generator.nextInt(drawingWidth):
117
             int y = generator.nextInt(drawingHeight);
             int width = generator.nextInt(drawingWidth - x);
119
             int height = generator.nextInt(drawingHeight - y);
120
             int r = generator.nextInt(256);
121
             int q = generator.nextInt(256);
122
123
             int b = generator.nextInt(256);
             writer.writeEmptyElement("rect");
124
             writer.writeAttribute("x", "" + x);
125
             writer.writeAttribute("v", "" + y);
126
             writer.writeAttribute("width", "" + width);
127
            writer.writeAttribute("height", "" + height);
128
             writer.writeAttribute("fill", "#%02x%02x".formatted(r, q, b));
129
```

```
130  }
131  writer.writeEndDocument(); // closes svg element
132  }
133 }
```

#### API javax.xml.stream.XMLOutputFactory

- static XMLOutputFactory newInstance()
   返回 XMLOutputFactory 类的一个实例。
- XMLStreamWriter createXMLStreamWriter(OutputStream in)
- XMLStreamWriter createXMLStreamWriter(OutputStream in, String characterEncoding)
- XMLStreamWriter createXMLStreamWriter(Writer in)
- XMLStreamWriter createXMLStreamWriter(Result in) 创建写出到给定流、写出器或 JAXP 结果的写出器。

#### API javax.xml.stream.XMLStreamWriter

- void writeStartDocument()
- void writeStartDocument(String xmlVersion)
- void writeStartDocument(String encoding, String xmlVersion)
   在文档的顶部写入 XML 处理指令。注意, encoding 参数只是用于写入这个属性,它不会设置输出的字符编码机制。
- void setDefaultNamespace(String namespaceURI)
- void setPrefix(String prefix, String namespaceURI)
   设置默认的命名空间,或者具有前缀的命名空间。这种声明的作用域只是当前元素,如果没有写明具体元素,其作用域为文档的根。
- void writeStartElement(String localName)
- void writeStartElement(String namespaceURI, String localName)
   写出一个开始标签,其中 namespaceURI 将用相关联的前缀来代替。
- void writeEndElement()关闭当前元素。
- void writeEndDocument()
   关闭所有打开的元素。
- void writeEmptyElement(String localName)
- void writeEmptyElement(String namespaceURI, String localName)
   写出一个自闭合的标签,其中 namespaceURI 将用相关联的前缀来代替。
- void writeAttribute(String localName, String value)
- void writeAttribute(String namespaceURI, String localName, String value)
   写出一个用于当前元素的属性,其中 namespaceURI 将用相关联的前缀来代替。
- void writeCharacters(String text)
   写出字符数据。

- void writeCData(String text)
   写出 CDATA 块。
- void writeDTD(String dtd)
   写出 dtd 字符串,该字符串需要包含一个 DOCTYPE 声明。
- void writeComment(String comment)
   写出一个注释。
- void close()关闭这个写出器。

#### 3.8.5 示例: 生成 SVG 文件

程序清单 3-9 是一个生成 XML 输出的典型程序。该程序绘制了一幅现代派绘画,即一组随机的彩色矩形(如图 3-3 所示)。我们使用可伸缩向量图形(Scalable Vector Graphics,

SVG)来保存作品。SVG是XML格式的,它使用设备无关的方式描述复杂图形。你可以在http://www.w3c.org/Graphics/SVG找到更多关于SVG的信息。要查看SVG文件,只需使用任何现在主流的浏览器。

该程序演示了两种产生 XML 的方式: 通过构建并保存 DOM 树,以及通过直接 用 StAX API 写出 XML。

我们并没有涉及 SVG 的细节。就我们的目的而言,我们只需要知道怎样表示一组彩色的矩形。下面是一个例子:

![](_page_187_Figure_10.jpeg)

图 3-3 生成的现代艺术品

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20000802//EN"
 "http://www.w3.org/TR/2000/CR-SVG-20000802/DTD/svg-20000802.dtd">
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="150">

</svg>

正如你看到的,每个矩形都被描述成了一个 rect 节点。它有位置、宽度、高度和填充色等属性,其中填充色以十六进制 RGB 值表示。

注释: SVG 大量使用了属性。实际上,某些属性相当复杂。例如,下面的 path 元素:

M是指"moveto"命令、L是指"lineto"、Z是指"closepath"(!)。显然,该数据格式的设计者不太信任 XML 表示结构化数据的能力。在你自己的 XML 格式中,你可能想使用元素来替代复杂的属性。

# *3.9 XSL <sup>换</sup>*

*XSL 换 XSLT 机制可以指定将XML文档 换为其他格式 则 例如 换为 文本、XHTML或任何其他 XML格式。XSLT 常 来将某 机器可 XML格式转译 为另一 机器可 XML格式 或 将XML 为 于人 格式。*

*你需要提供XSLT样式 它描 了 XML文档向某 其他格式 换 则。XSLT处 器将 人XML文档和 个样式 并产 所 出 如图34所 。*

![](_page_188_Figure_4.jpeg)

*<sup>图</sup>34<sup>应</sup> XSL <sup>换</sup>*

*XSLT规范很复杂 已 有很多书描 了 主 。我们不可 XSLT 全 性, 所以我们只 介 一个有代 性 例子。你可以在Don Box 人合著的Essential XML 一书 中找到更多 信息。XSLT规范可以在http://www.w3.org/TR/xslt 得。*

*假 我们想 把有 员 录 XML文件 换成HTML文件。 个 人文件*

```
<staff>
   <employee>
      <name>Carl Cracker</nan»e>
      <salary>75060</salary>
      <hiredate year=H1987M month="12" day="15_/>
   </employee>
   <employee>
      <name>Harry Hacker</name>
      <salary>50000</salary>
      <hiredate year=・1989・ months" 10' day="17>
   </employee>
   <employee>
      <name>Tony Tester</name>
      <salary>40000</salary>
      <hiredate year="1990" month=・3" day="15・/>
   </employee>
</staff>
我们希望 出是一张HTML 格
<table border=Ml">
<tr>
```

```
Carl Cracker$75000.01987-12-15
Harry Hacker$50000.0$1989-10-1
Tony Tester$40000.01990-3-15
具有转换模板的样式表形式如下:
<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet</pre>
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
  <xsl:output method="html"/>
  template1
  template2
</xsl:stylesheet>
```

在我们的例子中,xsl:output 元素将 method 设定为 HTML, 而其他有效的 method 设置包括 xml 和 text。

下面是一个典型的模板:

```
<xsl:template match="/staff/employee">
    <xsl:apply-templates/>
    </xsl:template>
```

match 属性的值是一个 XPath 表达式。该模板声明,每当看到 XPath 集 /staff/ employee 中的一个节点时,将做以下操作:

- 1. 产生字符串 >。
- 2. 在处理其子节点时,持续应用该模板。
- 3. 当处理完所有子节点后,产生字符串 。

换句话说,该模板会生成围绕每条雇员记录的 HTML 表格的行标记。

XSLT 处理器以检查根元素开始其处理过程。每当一个节点匹配某个模板时,就会应用该模板(如果匹配多个模板,就会使用最佳匹配的那个,详情请参见 http://www.w3.org/TR/xslt)。如果没有匹配的模板,处理器会执行默认操作。对于文本节点,默认操作是把它的内容囊括到输出中去。对于元素,默认操作是不产生任何输出,但会继续处理其子节点。

下面是一个用来转换雇员记录文件中的 name 节点的模板:

```
<xsl:template match="/staff/employee/name">
     <xsl:apply-templates/>
</xsl:template>
```

正如你所见,模板产生定界符 ... 
,并且让处理器递归访问 name 元素的子节点。它只有一个子节点,即文本节点。当处理器访问该节点时,它会提取出其中的文本内容(当然,前提是没有其他匹配的模板)。

如果想要把属性值复制到输出中去,就不得不再做一些稍微复杂的操作了。下面是一个 例子:

<xsl:template match="/staff/employee/hiredate">
 <xsl:value-of select="@year"/>-<xsl:value-of
 select="@month"/>-<xsl:value-of select="@day"/>
</xsl:template>

当处理 hiredate 节点时, 该模板会产生:

- 1. 字符串
- 2. year 属性的值
- 3. 一个连字符
- 4. month 属性的值
- 5. 一个连字符
- 6. day 属性的值
- 7. 字符串

xsl:value-of 语句用于计算节点集的字符串值,其中,节点集由 select 属性的 XPath 值指定。在这个例子中,路径是相对于当前正在处理的节点的相对路径。节点集通过将各个节点的字符串值连接起来而被转换成一个字符串。属性节点的字符串值就是它的值,文本节点的字符串值是它的内容,元素节点的字符串值是它的所有子节点(而不是其属性)的字符串值的连接。

程序清单 3-10 包含了将带有雇员记录的 XML 文件转换成 HTML 表格的样式表。

#### 程序清单 3-10 transform/makehtml.xsl

```
1 <?xml version="1.0" encoding="ISO-8859-1"?>
2
  <xsl:stylesheet
3
     xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
4
     version="1.0">
5
6
     <xsl:output method="html"/>
7
8
     <xsl:template match="/staff">
9
        <xsl:apply-templates/>
19
     </xsl:template>
11
12
     <xsl:template match="/staff/employee">
13
        <xsl:apply-templates/>
14
     </xsl:template>
15
16
     <xsl:template match="/staff/employee/name">
17
        <xsl:apply-templates/>
18
     </xsl:template>
19
28
     <xsl:template match="/staff/employee/salary">
21
        $<xsl:apply-templates/>
22
     </xsl:template>
23
```

```
24
      <xsl:template match="/staff/employee/hiredate">
25
         <xsl:value-of select="@year"/>-<xsl:value-of
26
         select="@month"/>-<xsl:value-of select="@day"/>
27
      </xsl:template>
28
29
30 </xsl:stylesheet>
```

程序清单 3-11 显示了一组不同的转换, 其输入是相同的 XML 文件, 输出是我们熟悉的 属性文件格式的纯文本:

```
employee.1.name=Carl Cracker
employee.1.salary=75000.0
employee.1.hiredate=1987-12-15
employee.2.name=Harry Hacker
employee.2.salary=50000.0
employee.2.hiredate=1989-10-1
employee.3.name=Tony Tester
employee.3.salary=40000.0
employee.3.hiredate=1990-3-15
```

#### 程序清单 3-11 transform/makeprop.xsl

```
1 <?xml version="1.0"?>
3 <xsl:stylesheet</pre>
      xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
4
      version="1.0">
      <xsl:output method="text" omit-xml-declaration="yes"/>
      <xsl:template match="/staff/employee">
10 employee.<xsl:value-of select="position()"</pre>
11 />.name=<xsl:value-of select="name/text()"/>
12 employee.<xsl:value-of select="position()"</pre>
13 />.salary=<xsl:value-of select="salary/text()"/>
14 employee.<xsl:value-of select="position()"</pre>
15 />.hiredate=<xsl:value-of select="hiredate/@year"</pre>
16 />-<xsl:value-of select="hiredate/@month"</pre>
17 />-<xsl:value-of select="hiredate/@day"/>
      </xsl:template>
18
19
20 </xsl:stylesheet>
```

该示例使用 position() 函数来产生以其父节点的角度来看的当前节点的位置。我们只要 切换样式表就可以得到一个完全不同的输出。这样,就可以安全地使用 XML 来描述数据了, 即便一些应用程序需要的是其他格式的数据,我们只要用 XSLT 来产生对应的可替代格式 即可。

在 Java 平台中产生 XML 的转换极其简单,只需为每个样式表设置一个转换器工厂,然 后得到一个转换器对象,并告诉它把一个源转换成结果。

```
var styleSheet = new File(filename);
var styleSource = new StreamSource(styleSheet);
Transformer t = TransformerFactory.newInstance().newTransformer(styleSource);
t.transform(source, result);
```

transform 方法的参数是 Source 和 Result 接口的实现类的对象。Source 接口有 4 个实现类:

DOMSource SAXSource StAXSource StreamSource

你可以从一个文件、流、阅读器或 URL 中构建 StreamSource 对象,或者从 DOM 树节点中构建 DOMSource 对象。例如,在上一节中,我们调用了如下的标识转换:

t.transform(new DOMSource(doc), result);

在示例程序中, 我们做了一些更有趣的事情。我们并不是从一个现有的 XML 文件开始工作, 而是产生一个 SAX XML 阅读器, 通过产生适合的 SAX 事件, 给人以解析 XML 文件的错觉。实际上, XML 阅读器读入的是一个如第 1 章所描述的平面文件, 输入文件看上去是这样的:

```
Carl Cracker|75000.0|1987|12|15
Harry Hacker|50000.0|1989|10|1
Tony Tester|40000.0|1990|3|15
```

处理输入时,XML 阅读器将产生 SAX 事件。下面是实现了 XMLReader 接口的 Employee-Reader 类的 parse 方法的一部分代码:

```
var attributes = new AttributesImpl();
handler.startDocument();
handler.startElement("", "staff", "staff", attributes);
boolean done = false:
while (!done)
   String line = in.readLine();
   if (line == null) done = true:
   else
      handler.startElement("", "employee", "employee", attributes);
      var tokenizer = new StringTokenizer(line, "|");
      handler.startElement("", "name", "name", attributes);
      String s = tokenizer.nextToken();
      handler.characters(s.toCharArray(), 0, s.length());
      handler.endElement("", "name", "name");
      handler.endElement("", "employee", "employee");
   }
handler.endElement("", rootElement, rootElement);
handler.endDocument();
用于转换器的 SAXSource 是从 XML 读入器中构建的:
```

t.transform(new SAXSource(new EmployeeReader(),

new InputSource(new FileInputStream(filename))), result);

这是将非 XML 的遗留数据转换成 XML 的一个小技巧。当然,大多数 XSLT 应用程序面对的都是 XML 格式的输入数据,只需要在一个 StreamSource 对象上调用 transform 方法即可,例如:

t.transform(new StreamSource(file), result);

其转换结果是 Result 接口的实现类的一个对象。Java 库提供了 3 个类:

DOMResult SAXResult StreamResult

要把结果存储到 DOM 树中,请使用 DocumentBuilder 产生一个新的文档节点,并将其包 装到 DOMResult 中:

```
Document doc = builder.newDocument();
t.transform(source, new DOMResult(doc));
```

要将输出保存到文件中, 请使用 StreamResult:

t.transform(source, new StreamResult(file));

程序清单 3-12 包含了完整的源代码。

#### 程序清单 3-12 transform/TransformTest.java

```
package transform;
3 import java.io.*;
4 import java.nio.file.*;
5 import java.util.*;
6 import javax.xml.transform.*;
7 import javax.xml.transform.sax.*;
8 import javax.xml.transform.stream.*;
9 import org.xml.sax.*;
import org.xml.sax.helpers.*;
11
12 /**
   * This program demonstrates XSL transformations. It applies a transformation to a set of
13
   * employee records. The records are stored in the file employee.dat and turned into XML
   * format. Specify the stylesheet on the command line, e.g.<br>
15
         java transform.TransformTest transform/makeprop.xsl
16
   * @version 1.05 2021-09-21
17
    * @author Cay Horstmann
18
19
20 public class TransformTest
21
      public static void main(String[] args) throws Exception
22
23
         Path path;
24
         if (args.length > 0) path = Path.of(args[0]);
25
         else path = Path.of("transform", "makehtml.xsl");
26
         try (InputStream styleIn = Files.newInputStream(path))
27
28
            var styleSource = new StreamSource(styleIn);
29
38
```

```
Transformer t = TransformerFactory.newInstance().newTransformer(styleSource);
31
32
            t.setOutputProperty(OutputKeys.INDENT, "yes");
            t.setOutputProperty(OutputKeys.METHOD, "xml");
33
            t.setOutputProperty("{http://xml.apache.org/xslt}indent-amount", "2");
34
35
            try (InputStream docIn = Files.newInputStream(Path.of("transform", "employee.dat")))
36
37
               t.transform(new SAXSource(new EmployeeReader(), new InputSource(docIn)),
38
                   new StreamResult(System.out));
39
41
42
43
44
45
    * This class reads the flat file employee.dat and reports SAX parser events to act as if it
46
    * was parsing an XML file.
47
48
   class EmployeeReader implements XMLReader
49
50
51
      private ContentHandler handler;
52
      public void parse(InputSource source) throws IOException, SAXException
53
54
55
         InputStream stream = source.getByteStream();
          var in = new BufferedReader(new InputStreamReader(stream));
56
         var atts = new AttributesImpl();
57
58
          if (handler == null) throw new SAXException("No content handler");
59
68
          handler.startDocument();
61
          handler.startElement("", "staff", "staff", atts);
62
          boolean done = false;
63
          while (!done)
64
65
             String line = in.readLine();
66
             if (line == null) done = true;
67
             else
68
69
                handler.startElement("", "employee", "employee", atts);
78
                var t = new StringTokenizer(line, "|");
71
72
                handler.startElement("", "name", "name", atts);
73
                String s = t.nextToken();
74
                handler.characters(s.toCharArray(), 0, s.length());
75
                handler.endElement("", "name", "name");
76
77
                handler.startElement("", "salary", "salary", atts);
78
79
                s = t.nextToken();
                handler.characters(s.toCharArray(), 0, s.length());
88
                handler.endElement("", "salary", "salary");
81
82
                atts.addAttribute("", "year", "year", "CDATA", t.nextToken());
83
                atts.addAttribute("", "month", "month", "CDATA", t.nextToken());
                atts.addAttribute("", "day", "day", "CDATA", t.nextToken());
85
```

```
handler.startElement("", "hiredate", "hiredate", atts);
86
               handler.endElement("", "hiredate", "hiredate");
87
               atts.clear();
88
89
               handler.endElement("", "employee", "employee");
91
         }
92
         handler.endElement("", "staff", "staff");
94
         handler.endDocument();
95
96
97
      public void setContentHandler(ContentHandler newValue)
98
99
100
         handler = newValue;
192
      public ContentHandler getContentHandler()
103
         return handler:
195
186
197
      // the following methods are just do-nothing implementations
108
      public void parse(String systemId) throws IOException, SAXException {}
      public void setErrorHandler(ErrorHandler handler) {}
110
111
      public ErrorHandler getErrorHandler() { return null; }
      public void setDTDHandler(DTDHandler handler) {}
      public DTDHandler getDTDHandler() { return null; }
113
      public void setEntityResolver(EntityResolver resolver) {}
114
      public EntityResolver getEntityResolver() { return null; }
      public void setProperty(String name, Object value) {}
116
117
      public Object getProperty(String name) { return null; }
      public void setFeature(String name, boolean value) {}
      public boolean getFeature(String name) { return false; }
119
120 }
```

# api javax.xml.transform.TransformerFactory

Transformer newTransformer(Source styleSheet)
 返回一个 transformer 类的实例,用来从指定的源中读取样式表。

# api javax.xml.transform.stream.StreamSource

- StreamSource(File f)
- StreamSource(InputStream in)
- StreamSource(Reader in)
- StreamSource(String systemID)
   自一个文件、流、阅读器或系统 ID(通常是相对或绝对 URL)构建一个数据流源。

# apr javax.xml.transform.sax.SAXSource

SAXSource(XMLReader reader, InputSource source)

构建一个 SAX 数据源,以便从给定输入源中获取数据,并使用给定的阅读器来解析输入数据。

#### API org.xml.sax.XMLReader

- void setContentHandler(ContentHandler handler)
   设置在输入被解析时会被告知解析事件的处理器。
- void parse(InputSource source)
   解析来自给定输入源的输入数据,并将解析事件发送到内容处理器。

## API javax.xml.transform.dom.DOMResult

DOMResult(Node n)
 自给定节点构建一个数据源。通常, n是一个新文档节点。

#### API org.xml.sax.helpers.AttributesImpl 1.4

void addAttribute(String uri, String lname, String qname, String type, String value)
 将一个属性添加到该属性集合中。

lname 参数是无前缀的本地名,而 qname 参数是带前缀的限定名,type 参数是 "CDATA" "ID" "IDREF" "IDREFS" "NMTOKEN" "NMTOKENS" "ENTITY" "ENTITIES" 或 "NOTATION" 之一

• void clear() 删除当前属性集合中的所有属性。

我们以该示例结束对 Java 库中的 XML 支持特性的讨论。现在,你应该对 XML 的强大功能有了很好的了解,尤其是它的自动解析、验证和强大的转换机制。当然,所有这些技术只有在你很好地设计了 XML 格式之后才能发挥作用。你必须确保这些设计出来的格式足够丰富,能够表达全部业务需求,随着时间的推移也依旧稳定,你的业务伙伴也愿意接受你的 XML 文档。这些问题要远比处理解析器、DTD 或转换更具挑战。

在下一章,我们将讨论在 Java 平台上的网络编程,从最基础的网络套接字开始,逐渐过渡到用于 E-mail 和万维网的更高层协议。

# *4*

- *▲ 接到服务器 HTTP客户*
- *▲ 取Web数据*

- *▲<sup>实</sup> 服务器 ▲发 E-mail*

*本 开头 分将 先回 一下 方 基本概念 然后 一步介 如何 写 接 服务 Java 序 并演 客户 和服务器是如何实 最后将介 如何 Java 序发 E-mail,以及如何从Web服务器 得信息。*

# *4.1 接到服务器*

*在下 各 中 你将学习如何 接到服务器 即先手工 telnet 接 然后 Java 序 接。 4.1.1 <sup>使</sup> telnet*

*telnet是一 于 常强大 工具 可以在命令shell中 入telnet来启 动它。*

*H <sup>注</sup> <sup>在</sup>Windows<sup>中</sup> 需要激活telnet。 激活它 <sup>到</sup>"控制 <sup>板</sup>" <sup>择</sup>" <sup>序</sup>" 单击"打开/<sup>关</sup> Windows <sup>性</sup>" 然后 <sup>择</sup>"Telnet客户 "<sup>复</sup> <sup>框</sup>。Windows <sup>火</sup> 墙将会 止我们在本 中使用的很多网络端口 你可 员 户才 对它 们 。*

*你可 曾 使 telnet来 接 机 ,但其实你也可以 它与因 主机所提供*

*其他服务 信。下 是一个可以操作 例子。 入*

*telnet time-a.nist.gov <sup>13</sup>*

*如图44所 你可以得到与下面这一 行相似 信息*

*<sup>57488</sup> 16-B4-1 04:23:66 <sup>5</sup> 610.5 UTC(NIST) \**

*上 例子 明了什么 它 明你已 接到了大多数UNIX 机 支持 "当<sup>H</sup> 时 "服务。 你刚才所 接 台服务器*

![](_page_197_Picture_18.jpeg)

*图4-1 "当H时 "服务的输出*

就是由美国国家标准与技术研究所运维的,这家研究所负责提供铯原子钟的计量时间。(当然,由于网络延迟的缘故,原子钟反馈过来的时间并不完全准确。)

按照惯例,"当日时间"服务总是连接到端口13。

直 注释:在网络术语中,端口并不是指物理设备,而是为了便于实现服务器与客户端之间的通信所使用的抽象概念(见图 4-2)。

![](_page_198_Figure_4.jpeg)

图 4-2 连接到服务器端口的客户端

运行在远程计算机上的服务器软件不停地等待那些希望与端口 13 连接的网络请求。当远程计算机上的操作系统接收到一个请求与端口 13 连接的网络数据包时,它便唤醒正在监听网络连接请求的服务器进程,并为两者建立连接。这种连接将一直保持下去,直到被其中任何一方中止。

当你开始与 time-a.nist.gov 在端口 13 上建立 telnet 会话时,网络软件中有一段代码非常清楚地知道应该将字符串"time-a.nist.gov"转换为正确的 IP 地址 129.6.15.28。随后,telnet 软件发送一个连接请求给该地址,请求一个到端口 13 的连接。一旦建立连接,远程程序便发送回一行数据,然后关闭该连接。当然,一般而言,客户端和服务器在其中一方关闭连接之前,会进行更多的对话。

下面是另一个同类型的试验,但它更加有趣。请执行以下操作:

telnet horstmann.com 80

然后非常仔细地键入以下内容:

GET / HTTP/1.1 Host: horstmann.com blank line

#### 也就是在末尾按两次 Enter 键。

图 4-3 显示了以上操作的响应结果。它看上去应该是你非常熟悉的内容——你得到的是一个 HTML 格式的文本页,即 Cay Horstmann 的主页。

```
-S telnet horstmann.com 80
Trying 67.210,118.65.,
Connected to horstmann.com.
Escape character is '^]',
GET / HTTP/1.1
Host: horstmann.com
HTTP/1.1 200 OK
Date: Sun, 10 Apr 2016 04:36:27 GMT
Server: Apache/2.2.24 (Unix) mod ssl/2.2.24 OpenSSL/0.9.8e-fips-rhel5 mod auth p
assthrough/2.1 mod bwlimited/1.4 mod fcgid/2.3.6 Sun-ONE-ASP/4.0.3
Last-Modified: Thu, 17 Mar 2016 18:32:18 GMT
ETag: "2590e1c-1c47-52e42d9a8f080"
Accept-Ranges: bytes
Content-Length: 7239
Content-Type: text/html
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/x</pre>
html1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"><head>
  <title>Cay Horstmann's Home Page</title>
  <link href="styles.css" rel="stylesheet" type="text/css"/>
```

图 4-3 使用 telnet 访问 HTTP 端口

上述操作与 Web 浏览器访问某个网页所经历的过程是完全一致的,它使用 HTTP 向服务器请求 Web 页面。当然,浏览器能够更精致地显示 HTML 代码。

注释:如果一台 Web 服务器用相同的 IP 地址为多个域提供宿主环境,那么在连接这台 Web Server 时,就必须提供 Host 键/值对。如果服务器只为单个域提供宿主环境,则可以忽略该键/值对。

#### 4.1.2 用 Java 连接到服务器

程序清单 4-1 是我们的第一个网络程序。它的作用与我们使用 telnet 工具是相同的,即连接到某个端口并打印出它所找到的信息。

#### 程序清单 4-1 socket/SocketTest.java

```
1 package socket;
2
3 import java.io.*;
4 import java.net.*;
5 import java.nio.charset.*;
6 import java.util.*;
7
8 /**
* This program makes a socket connection to the atomic clock in Boulder, Colorado, and
* prints the time that the server sends.
   * @version 1.22 2018-03-17
   * @author Cay Horstmann
12
   */
13
14 public class SocketTest
15 {
      public static void main(String[] args) throws IOException
16
17
```

```
try (var s = new Socket("time-a.nist.gov", 13);
```

下面是这个简单程序的关键代码:

var s = new Socket("time-a.nist.gov", 13);

第一行代码用于打开一个套接字,它也是网络软件中的一个抽象概念,负责启动该程序内部和外部之间的通信。我们将远程地址和端口号传递给套接字的构造器,如果连接失败,它将抛出一个UnknownHostException异常;如果存在其他问题,它将抛出一个IOException异常。因为UnknownHostException是 IOException的一个子类,并且这只是一个示例程序,所以我们在这里仅仅捕获超类的异常。

一旦套接字被打开, java.net.Socket类中的 getInputStream方法就会返回一个 InputStream 对象,该对象可以像其他任何流对象一样使用。而一旦获取了这个流,该程序将直接把每一行打印到标准输出。这个过程将一直持续到流发送完毕且服务器断开连接为止。

该程序只适用于非常简单的服务器,比如"当日时间"之类的服务。在比较复杂的网络程序中,客户端发送请求数据给服务器,而服务器可能在响应结束时并不立刻断开连接。在本章的若干个示例程序中,都会看到我们是如何实现这种行为的。

Socket 类非常简单易用,因为 Java 库隐藏了建立网络连接和通过网络连接发送数据的复杂过程。实际上,java.net 包提供的编程接口与操作文件时所使用的接口基本相同。

這 注释:本书所介绍的内容仅覆盖了TCP(传输控制协议)网络协议。Java平台另外还支持UDP(用户数据报协议)协议,该协议可以用于发送数据包(也称为数据报),它的开销要比TCP少得多。UDP有一个重要的缺点:数据包无须按照顺序传递到接收应用程序,它们甚至可能在传输过程中全部丢失。UDP让数据包的接收者自己负责对它们进行排序,以及请求发送者重新发送那些丢失的数据包。UDP比较适合于那些可以忍受数据包丢失的应用,例如用于音频流和视频流的传输,或者用于连续测量的应用领域。

#### API java.net.Socket 1.0

- Socket(String host, int port)
   构建一个套接字,用来连接给定的主机和端口。
- InputStream getInputStream()

OutputStream getOutputStream()
 获取可以从套接字中读取数据的流,以及可以向套接字写出数据的流。

#### 4.1.3 套接字超时

从套接字读取信息时,在有数据可供访问之前,读操作将会被阻塞。如果此时主机不可达,那么应用将要等待很长的时间,并且会因受底层操作系统的限制而最终会导致超时。

对于不同的应用,应该确定合理的超时值,然后调用 setSoTimeout 方法设置这个超时值(单位: 毫秒)。

```
var s = new Socket(. . .);
s.setSoTimeout(10000); // time out after 10 seconds
```

如果已经为套接字设置了超时值,并且之后的读操作和写操作在没有完成之前就超过了时间限制,那么这些操作就会抛出 SocketTimeoutException 异常。你可以捕获这个异常,并对超时做出反应。

```
try
{
    InputStream in = s.getInputStream(); // read from in
    . . .
}
catch (SocketTimeoutException e)
{
    react to timeout
}
```

对于写操作是没有任何超时的。

另外还有一个超时问题是必须解决的。下面这个构造器:

Socket(String host, int port)

会一直无限期地阻塞下去,直到建立了到达主机的初始连接为止。

可以通过先构建一个无连接的套接字, 然后再使用一个超时来进行连接的方式解决这个问题。

```
var s = new Socket();
s.connect(new InetSocketAddress(host, port), timeout);
```

如果你希望允许用户在任何时刻都可以中断套接字连接,请查看 4.2.4 节。

# api java.net.Socket 1.0

- Socket() 1.1 创建一个还未被连接的套接字。
- void connect(SocketAddress address) 1.4
   将该套接字连接到给定的地址。
- void connect(SocketAddress address, int timeoutInMilliseconds) 1.4 将套接字连接到给定的地址。如果在给定的时间内没有响应,则返回。
- void setSoTimeout(int timeoutInMilliseconds)

设置该套接字上读请求的阻塞时间。如果超出给定时间,则抛出一个 SocketTime outException 异常。

- boolean isConnected() 1.4
   如果该套接字已被连接,则返回 true。
- boolean isClosed() 1.4
   如果该套接字已被关闭,则返回 true。

#### 4.1.4 因特网地址

通常,不用过多考虑因特网地址的问题,它们是用一串数字表示的主机地址,一个因特网地址由 4 个字节组成(在 IPv6 中是 16 个字节),比如 129.6.15.28。但是,如果需要在主机名和因特网地址之间进行转换,那么就可以使用 InetAddress 类。

java.net 包支持 IPv6 格式的因特网地址, 前提是主机的操作系统也要支持。 静态的 getByName 方法可以返回代表某个主机的 InetAddress 对象。例如,

InetAddress address = InetAddress.getByName("time-a.nist.gov");

将返回一个 InetAddress 对象,该对象封装了一个 4 字节的序列: 129.6.15.28。然后,可以使用 getAddress 方法来访问这些字节:

byte[] addressBytes = address.getAddress();

一些访问量较大的主机名通常会对应于多个因特网地址,以实现负载均衡。例如,在撰写本书时,主机名 google.com 就对应着 12 个不同的因特网地址。当访问主机时,会随机选取其中的一个。可以通过调用 getAllByName 方法来获得所有主机:

InetAddress[] addresses = InetAddress.getAllByName(host);

最后需要说明的是,有时我们可能需要本地主机的地址。如果只是要求得到 local host 的地址,那总会得到本地回环地址 127.0.0.1,但是其他程序无法用这个地址来连接到这台机器上。此时,可以使用静态的 getLocal Host 方法来得到本地主机的地址:

InetAddress address = InetAddress.getLocalHost();

程序清单 4-2 是一段比较简单的程序代码。如果不在命令行中设置任何参数,那么它将打印出本地主机的因特网地址。反之,如果在命令行中指定了主机名,那么它将打印出该主机的所有因特网地址,例如:

java inetAddress/InetAddressTest www.horstmann.com

#### 程序清单 4-2 inetAddress/InetAddressTest.java

```
package inetAddress;\nimport java.io.*;\nimport java.net.*;
/**
```

\* This program demonstrates the InetAddress class. Supply a host name as command-line

```
* argument, or run without command-line arguments to see the address of the local host.
   * @version 1.02 2012-06-05
10 * @author Cay Horstmann
11 */
12 public class InetAddressTest
13 {
      public static void main(String[] args) throws IOException
14
15
         if (args.length > 0)
16
17
            String host = args[0];
18
            InetAddress[] addresses = InetAddress.getAllByName(host);
19
            for (InetAddress a : addresses)
20
               System.out.println(a);
21
22
         7
         else
23
24
            InetAddress localHostAddress = InetAddress.getLocalHost();
25
            System.out.println(localHostAddress);
26
27
28
      }
29 }
```

#### API java.net.InetAddress 1.0

- static InetAddress getByName(String host)
- static InetAddress[] getAllByName(String host)
   为给定的主机名创建一个 InetAddress 对象,或者一个包含了该主机名所对应的所有因特网地址的数组。
- static InetAddress getLocalHost()
   为本地主机创建一个 InetAddress 对象。
- byte[] getAddress()返回一个包含数字型地址的字节数组。
- String getHostAddress()
   返回一个由十进制数组成的字符串,各数字间用圆点符号隔开,例如,"129.6.15.28"。
- String getHostName()
   返回主机名。

# 4.2 实现服务器

在上一节中,我们已经实现了一个基本的网络客户端,并且用它从因特网上获取了数据。在这一节中,我们将实现一个简单的服务器,它可以向客户端发送信息。

#### 4.2.1 服务器套接字

一旦启动了服务器程序,它便会等待某个客户端连接到它的端口。在我们的示例程序

中,我们选择端口号 8189,因为所有标准服务都不使用这个端口。ServerSocket 类用于建立 套接字。在我们的示例中,下面这行命令:

var s = new ServerSocket(8189);

用于建立一个负责监控端口 8189 的服务器。以下命令:

Socket incoming = s.accept();

用于告诉程序不停地等待,直到有客户端连接到这个端口。一旦有人通过网络发送了正确的连接请求,并以此连接到了端口上,该方法就会返回一个表示连接已经建立的 Socket 对象。你可以使用这个对象来得到输入流和输出流,代码如下:

InputStream inStream = incoming.getInputStream();
OutputStream outStream = incoming.getOutputStream();

服务器发送给服务器输出流的所有信息都会成为客户端程序的输入,同时来自客户端程序的所有输出都会被包含在服务器输入流中。

因为在本章的所有示例程序中,我们都要通过套接字来发送文本,所以我们将流转换成 扫描器和写人器。

var in = new Scanner(inStream, StandardCharsets.UTF\_8);
var out = new PrintWriter(new OutputStreamWriter(outStream, StandardCharsets.UTF\_8),

以下代码将给客户端发送一条问候信息:

out.println("Hello! Enter BYE to exit.");

当使用 telnet 通过端口 8189 连接到这个服务器程序时,将会在终端屏幕上看到上述问候信息。

在这个简单的服务器程序中,它只是读取客户端输入,每次读取一行,并回送这一行。 这表明程序接收到了客户端的输入。当然,实际应用中的服务器都会对输入进行计算并返回 处理结果。

String line = in.nextLine();
out.println("Echo: " + line);\nif (line.strip().equals("BYE")) done = true;

在代码的最后, 我们关闭了连接进来的套接字。

incoming.close();

这就是整个示例代码的大致情况。每一个服务器程序,比如一个 HTTP Web 服务器,都会不间断地执行下面这个循环:

- 1. 通过输入数据流从客户端接收一个命令("get me this information")。
- 2. 解码这个客户端命令。
- 3. 收集客户端所请求的信息。
- 4. 通过输出数据流发送信息给客户端。

程序清单 4-3 给出了这个程序的完整代码。

#### 程序清单 4-3 server/EchoServer.java

```
1 package server;
3 import java.io.*;
4 import java.net.*;
5 import java.nio.charset.*;
6 import java.util.*;
7
8 /**
   * This program implements a simple server that listens to port 8189 and echoes back all
   * client input.
    * @version 1.22 2018-03-17
    * @author Cay Horstmann
12
14 public class EchoServer
15
      public static void main(String[] args) throws IOException
17
         // establish server socket
18
         try (var s = new ServerSocket(8189))
19
28
            // wait for client connection
            try (Socket incoming = s.accept())
22
23
                InputStream inStream = incoming.getInputStream();
24
                OutputStream outStream = incoming.getOutputStream();
25
26
                try (var in = new Scanner(inStream, StandardCharsets.UTF 8))
27
28
                   var out = new PrintWriter(
                      new OutputStreamWriter(outStream, StandardCharsets.UTF 8),
30
                      true /* autoFlush */);
31
                   out.println("Hello! Enter BYE to exit.");
33
34
                   // echo client input
                   boolean done = false:
36
                   while (!done && in.hasNextLine())
37
                      String line = in.nextLine();
39
                      out.println("Echo: " + line);
49
                      if (line.strip().equals("BYE")) done = true;
41
42
43
            }
44
         }
45
      }
46
47 }
```

如果想要试一下这个例子,就请编译并运行这个程序,然后使用 telnet 连接到服务器 localhost (或 IP 地址 127.0.0.1)和端口 8189。

如果你直接连接到因特网上,那么世界上任何人都可以访问到你的回送服务器,只要他

们知道你的 IP 地址和端口号。

当你连接到该端口时,将看到如图 4-4 所示的信息:

Hello! Enter BYE to exit.

```
| Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | Second | S
```

图 4-4 访问一个回送服务器

可以随意键入一条信息,然后观察屏幕上的回送信息。输入 BYE (全为大写字母)可以断 开连接,同时,服务器程序也会终止运行。

#### API java.net.ServerSocket

- ServerSocket(int port)
   创建一个监听端口的服务器套接字。
- Socket accept()

等待连接。该方法阻塞(即,使之空闲)当前线程直到建立连接为止。该方法返回一个 Socket 对象,程序可以通过这个对象与连接中的客户端进行通信。

• void close() 关闭服务器套接字。

# 4.2.2 为多个客户端服务

前面例子中的简单服务器存在一个问题。假设我们希望有多个客户端同时连接到我们的服务器上。通常,服务器总是不间断地运行在服务器计算机上,来自整个因特网的用户希望同时使用服务器。前面的简单服务器会提供对客户端连接的支持,使得任何一个客户端都可以因长时间地连接服务而独占服务,其实我们可以运用线程的魔力把这个问题解决得更好。

每当程序建立一个新的套接字连接,也就是说当调用 accept()时,将会启动一个新的线程来处理服务器和该客户端之间的连接,而主程序将立即返回并等待下一个连接。为了实现这种机制,服务器应该具有类似以下代码的循环操作:

```
while (true)
{
   Socket incoming = s.accept();
   var r = new ThreadedEchoHandler(incoming);
```

```
var t = new Thread(r);
t.start();
}
```

ThreadedEchoHandler 类实现了 Runnable 接口,而且在它的 run 方法中包含了与客户端循环通信的代码。

```
class ThreadedEchoHandler implements Runnable
{
    public void run()
    {
        try (InputStream inStream = incoming.getInputStream();
```

由于每一个连接都会启动一个新的线程,因而多个客户端就可以同时连接到服务器了。 对此可以做个简单的测试:

- 1. 编译和运行服务器程序(程序清单 4-4)。
- 2. 如图 4-5 所示, 打开数个 telnet 窗口。
- 3. 在这些窗口之间切换,并键入命令。注意你可以同时通过这些窗口进行通信。
- 4. 当完成之后, 切换到启动服务器程序的窗口, 并使用 CTRL+C 强行关闭它。

![](_page_207_Figure_10.jpeg)

图 4-5 多个同时通信的 telnet 窗口

註釋:在这个程序中,我们为每个连接生成一个单独的线程。这种方法并不能满足高性能服务器的要求。为使服务器实现更高的吞吐量,可以使用 java.nio 包中的一些特性。详情请参见以下链接: http://www.ibm.com/developerworks/java/library/j-javaio。

#### 程序清单 4-4 threaded/ThreadedEchoServer.java

```
1 package threaded;
2
3 import java.io.*;
4 import java.net.*;
5 import java.nio.charset.*;
6 import java.util.*;
7
  /**
8
    * This program implements a multithreaded server that listens to port 8189 and echoes back
9
   * all client input.
    * @author Cay Horstmann
11
   * @version 1.23 2018-03-17
12
13
   public class ThreadedEchoServer
14
   {
15
      public static void main(String[] args )
16
17
         try (var s = new ServerSocket(8189))
18
19
            int i = 1;
28
21
            while (true)
22
23
                Socket incoming = s.accept();
24
                System.out.println("Spawning " + i);
25
                Runnable r = new ThreadedEchoHandler(incoming);
26
                var t = new Thread(r);
27
                t.start();
28
                1++;
29
            }
38
         }
31
         catch (IOException e)
32
33
             e.printStackTrace();
34
35
36
   }
37
38
39
    * This class handles the client input for one server socket connection.
48
41
   class ThreadedEchoHandler implements Runnable
42
43
      private Socket incoming;
44
45
46
         Constructs a handler.
47
```

```
@param incomingSocket the incoming socket
48
49
      public ThreadedEchoHandler(Socket incomingSocket)
50
51
         incoming = incomingSocket;
52
53
54
      public void run()
55
56
         try (InputStream inStream = incoming.getInputStream();
57
                OutputStream outStream = incoming.getOutputStream();
58
                var in = new Scanner(inStream, StandardCharsets.UTF 8);
59
                var out = new PrintWriter(
68
                   new OutputStreamWriter(outStream, StandardCharsets.UTF 8),
61
                   true /* autoFlush */))
62
         {
63
             out.println( "Hello! Enter BYE to exit." );
64
65
             // echo client input
66
             boolean done = false:
67
             while (!done && in.hasNextLine())
68
59
                String line = in.nextLine():
78
                out.println("Echo: " + line);
71
                if (line.strip().equals("BYE"))
72
73
                   done = true;
74
          }
75
          catch (IOException e)
76
77
             e.printStackTrace();
78
79
80
81 }
```

#### 4.2.3 半关闭

半关闭(half-close)提供了这样一种能力:套接字连接的一端可以终止其输出,同时仍旧可以接收来自另一端的数据。

这是一种很典型的情况,例如我们向服务器传输数据,但是一开始并不知道要传输多少数据。在向文件写数据时,我们只需在数据写人后关闭文件即可。但是,如果关闭一个套接字,那么与服务器的连接将立刻断开,因而也就无法读取服务器的响应了。

使用半关闭的方法就可以解决上述问题。可以通过关闭一个套接字的输出流来表示发送 给服务器的请求数据已经结束,但是必须保持输入流处于打开状态。

如下代码演示了如何在客户端使用半关闭方法:

```
try (var socket = new Socket(host, port))
{
  var in = new Scanner(socket.getInputStream(), StandardCharsets.UTF_8);
  var writer = new PrintWriter(socket.getOutputStream());
```

```
// send request data
writer.print(. . .);
writer.flush();
socket.shutdownOutput();
// now socket is half-closed
// read response data
while (in.hasNextLine() != null)
{
    String line = in.nextLine();
    . . .
}
```

服务器端将读取输入信息,直至到达输入流的结尾,然后它再发送响应。

当然,该协议只适用于一次性(one-shot)的服务,例如 HTTP 服务,在这种服务中,客户端连接服务器,发送一个请求,捕获响应信息,然后断开连接。

#### API java.net.Socket

- void shutdownOutput() 1.3将输出流设为"流结束"。
- void shutdownInput() 1.3将输入流设为"流结束"。
- boolean isOutputShutdown() 1.4
   如果输出已被关闭,则返回 true。
- boolean isInputShutdown() 1.4
   如果输入已被关闭,则返回 true。

### 4.2.4 可中断套接字

当连接到一个套接字时,当前线程将会被阻塞直到建立连接或产生超时为止。同样地, 当通过套接字读数据时,当前线程也会被阻塞直到操作成功或产生超时为止。

在交互式的应用中,也许会考虑为用户提供一个选项,用以取消那些看似不会产生结果的 连接。但是,当线程因套接字无法响应而发生阻塞时,则无法通过调用 interrupt 来解除阻塞。

为了中断套接字操作,可以使用 java.nio 包提供的一个特性——SocketChannel 类。可以使用如下方法打开 SocketChannel:

SocketChannel channel = SocketChannel.open(new InetSocketAddress(host, port));

通道 (channel) 并没有与之相关联的流。实际上,它所拥有的 read 和 write 方法都是通过使用 Buffer 对象来实现的 (关于 NIO 缓冲区的相关信息请参见第 2 章)。Readable-ByteChannel 接口和 WritableByteChannel 接口都声明了这两个方法。

如果不想处理缓冲区,可以使用 Scanner 类从 SocketChannel 中读取信息,因为 Scanner 有一个带 ReadableByteChannel 参数的构造器:

var in = new Scanner(channel, StandardCharsets.UTF 8);

通过调用静态方法 Channels.newOutputStream,可以将通道转换成输出流。

OutputStream outStream = Channels.newOutputStream(channel);

上述操作就是所有要做的事情。当线程正在执行打开、读取或写入操作时,如果线程发生中断,那么这些操作将不会陷入阻塞,而是以抛出异常的方式结束。

程序清单 4-5 的程序对比了可中断套接字和阻塞套接字: 服务器将连续发送数字, 并在每发送十个数字之后停滞一下。点击两个按钮中的任何一个, 都会启动一个线程来连接服务器并打印输出。第一个线程使用可中断套接字, 而第二个线程使用阻塞套接字。如果在第一批的十个数字的读取过程中点击 "Cancel"按钮, 这两个线程都会中断。

#### 程序清单 4-5 interruptible/InterruptibleSocketTest.java

```
package interruptible;
3 import java.awt.*;
4 import java.awt.event.*;
  import java.util.*;
   import java.net.*;
   import java.io.*;
8 import java.nio.charset.*;
9 import java.nio.channels.*;
import javax.swing.*;
11
12 /**
   * This program shows how to interrupt a socket channel.
13
   * @author Cay Horstmann
14
    * @version 1.05 2018-03-17
15
16
   public class InterruptibleSocketTest
17
18
      public static void main(String[] args)
19
20
         EventQueue.invokeLater(() ->
21
22
               var frame = new InterruptibleSocketFrame();
23
               frame.setTitle("InterruptibleSocketTest");
24
               frame.setDefaultCloseOperation(JFrame.EXIT ON CLOSE);
25
               frame.setVisible(true);
26
27
            }):
      }
28
  }
29
38
   class InterruptibleSocketFrame extends JFrame
  {
32
      private Scanner in;
33
      private JButton interruptibleButton;
34
      private JButton blockingButton;
35
      private JButton cancelButton:
36
      private JTextArea messages;
37
      private TestServer server;
38
```

```
private Thread connectThread;
39
48
      public InterruptibleSocketFrame()
41
42
         var northPanel = new JPanel();
43
          add(northPanel, BorderLayout.NORTH);
44
45
          final int TEXT ROWS = 20;
46
          final int TEXT COLUMNS = 60;
47
          messages = new JTextArea(TEXT ROWS, TEXT COLUMNS);
48
          add(new JScrollPane(messages));
49
58
          interruptibleButton = new JButton("Interruptible");
51
          blockingButton = new JButton("Blocking");
52
53
          northPanel.add(interruptibleButton);
54
          northPanel.add(blockingButton);
55
56
          interruptibleButton.addActionListener(event ->
57
58
                interruptibleButton.setEnabled(false);
50
                blockingButton.setEnabled(false);
68
                cancelButton.setEnabled(true);
61
                connectThread = new Thread(() ->
62
63
54
                      try
                       {
65
                          connectInterruptibly();
66
                      }
67
                       catch (IOException e)
68
                          messages.append("\nInterruptibleSocketTest.connectInterruptibly: " + e);
78
71
72
                   });
                connectThread.start();
73
             1):
74
75
          blockingButton.addActionListener(event ->
75
77
                interruptibleButton.setEnabled(false);
78
                blockingButton.setEnabled(false);
79
                cancelButton.setEnabled(true);
89
                connectThread = new Thread(() ->
81
82
                       try
83
84
                          connectBlocking():
85
                       1
86
                       catch (IOException e)
87
88
                          messages.append("\nInterruptibleSocketTest.connectBlocking: " + e);
89
QA.
                    });
91
                connectThread.start();
92
```

```
});
93
94
         cancelButton = new JButton("Cancel");
95
         cancelButton.setEnabled(false);
         northPanel.add(cancelButton);
97
98
         cancelButton.addActionListener(event ->
             1
188
                connectThread.interrupt();
                cancelButton.setEnabled(false);
101
             });
         server = new TestServer();
183
         new Thread(server).start();
104
         pack();
105
196
107
108
       * Connects to the test server, using interruptible I/O
189
110
      public void connectInterruptibly() throws IOException
111
112
113
         messages.append("Interruptible:\n");
         try (SocketChannel channel
114
                = SocketChannel.open(new InetSocketAddress("localhost", 8189)))
115
             in = new Scanner(channel, StandardCharsets.UTF 8);
117
118
             while (!Thread.currentThread().isInterrupted())
                messages.append("Reading");
120
                if (in.hasNextLine())
121
122
                   String line = in.nextLine();
123
124
                   messages.append(line);
                   messages.append("\n");
126
127
         finally
129
             EventQueue.invokeLater(() ->
131
                {
132
                   messages.append("Channel closed\n");
                   interruptibleButton.setEnabled(true);
134
                   blockingButton.setEnabled(true);
135
                });
136
137
      }
138
139
148
141
       * Connects to the test server, using blocking I/O
142
      public void connectBlocking() throws IOException
143
144
         messages.append("Blocking:\n");
145
         try (var sock = new Socket("localhost", 8189))
146
```

```
147
             in = new Scanner(sock.getInputStream(), StandardCharsets.UTF_8);
148
             while (!Thread.currentThread().isInterrupted())
150
                messages.append("Reading");
151
                if (in.hasNextLine())
153
                   String line = in.nextLine();
154
                   messages.append(line);
                   messages.append("\n");
156
157
             }
158
159
          finally
160
161
             EventQueue.invokeLater(() ->
162
163
                {
                   messages.append("Socket closed\n");
164
                   interruptibleButton.setEnabled(true);
165
                   blockingButton.setEnabled(true);
                });
167
168
          }
      }
169
179
171
        * A multithreaded server that listens to port 8189 and sends numbers to the client,
172
        * simulating a hanging server after 10 numbers.
173
        */
174
       class TestServer implements Runnable
175
176
          public void run()
177
178
             try (var s = new ServerSocket(8189))
179
180
                while (true)
181
                {
182
                    Socket incoming = s.accept();
183
                    Runnable r = new TestServerHandler(incoming);
184
                    new Thread(r).start();
185
                }
185
187
             catch (IOException e)
188
189
                messages.append("\nTestServer.run: " + e);
198
191
192
       }
193
194
195
        * This class handles the client input for one server socket connection.
196
197
       class TestServerHandler implements Runnable
198
199
200
          private Socket incoming;
```

```
private int counter;
201
202
203
           * Constructs a handler.
204
           * @param i the incoming socket
295
206
          public TestServerHandler(Socket i)
207
288
             incoming = i;
209
          }
210
211
          public void run()
212
213
             try
214
215
                 try
216
217
                 {
                    OutputStream outStream = incoming.getOutputStream();
218
                    var out = new PrintWriter(
219
                       new OutputStreamWriter(outStream, StandardCharsets.UTF 8),
220
                        true /* autoFlush */);
221
                    while (counter < 100)
222
223
                        counter++:
224
                       if (counter <= 10) out.println(counter);</pre>
225
                       Thread.sleep(100);
226
227
228
                 }
                 finally
229
238
                    incoming.close():
231
                    messages.append("Closing server\n");
233
             }
234
              catch (Exception e)
235
236
                 messages.append("\nTestServerHandler.run: " + e);
237
238
239
240
241 }
```

但是,在第一批十个数字之后,就只能中断第一个线程了,第二个线程将保持阻塞直到服务器最终关闭连接(参见图 4-6)。

# API java.net.InetSocketAddress

- InetSocketAddress(String hostname, int port)
   用给定的主机和端口参数创建一个地址对象,并在创建过程中解析主机名。如果主机名不能被解析,那么该地址对象的 unresolved 属性将被设为 true。
- boolean isUnresolved()
   如果不能解析该地址对象,则返回 true。

![](_page_216_Picture_1.jpeg)

图 4-6 中断一个套接字

#### API java.nio.channels.SocketChannel

static SocketChannel open(SocketAddress address)
 打开一个套接字通道,并将其连接到远程地址。

#### API java.nio.channels.Channels

- static InputStream newInputStream(ReadableByteChannel channel)
   创建一个输入流,用以从指定的通道读取数据。
- static OutputStream newOutputStream(WritableByteChannel channel) 创建一个输出流,用以向指定的通道写入数据。

# 4.3 获取 Web 数据

为了在 Java 程序中访问 Web 服务器,你可能希望在更高的级别上进行处理,而不只是 创建套接字连接和发送 HTTP 请求。在下面的各个小节中,我们将讨论专用于此目的的 Java 类库中的各个类。

#### 4.3.1 URL和URI

URL 和 URLConnection 类封装了大量复杂的实现细节,这些细节涉及如何从远程站点获取信息。例如,可以自一个字符串构建一个 URL 对象:

var url = new URL(urlString);

如果只是想获得该资源的内容,可以使用 URL 类中的 openStream 方法。该方法将产生一个 InputStream 对象,然后就可以按照一般的用法来使用这个对象了,比如用它构建一个 Scanner 对象:

InputStream inStream = url.openStream();
var in = new Scanner(inStream, StandardCharsets.UTF 8);

java.net 包对统一资源定位符(Uniform Resource Locator, URL)和统一资源标识符(Uniform Resource Identifier, URI)进行了非常有用的区分。

*URI是个 法 构 包含 来指定Web 源 字 串 各 成 分。URL是 URI 一个 例 它包含了 于定位Web 源 够信息。其他URI,比如*

*mailto:cay@horstmann•com*

*则不属于定位 因为根据 标 我们无法定位任何数据。像 样 URI我们 为URN Uniform Resource Name, 一 源名 <sup>o</sup>*

*在Java 库中 URI 并不包含任何 于 标 指向 源 方法 它 唯一作 就是 析。但是 URL 可以打开一个 接到 源 流。因此 URL 只 作 于 些Java 库 如何处 模式 例如http: https: ftp: 本地文件 file: 和JAR文件 jar:*

*想了 为什么对URI进行解析并 4淳一桩 可以 一下URL会变得多么复杂。例如*

*http:/google・ com?q=Beach+Chalet*

*ftp://username:password@ftp•yourserver•con/pub/file•txt*

*URI 出了标 些标 则。一个URI具有以下句法*

*[scheme: ]schemeSpedficPart [^fragment]*

*上式中 [...]表示可选部分 并且标识符中可以包含 和#。*

*包含scheme: 分 URI 为 对URI;否则 为 对URI*

*如果 对URI schemeSpecificPart不是以/开头 我们就 它是不 明 。例如*

*mailto:cay@horstmann.com*

*所有 对 明URI和所有 对URI 是分层 hierarchical 。例如*

*http://horstmann•com/index.html ../../java/net/Socket.html#Socket*

*一个分层URI schemeSpecificPart具有以下 构*

*[//authority] [path] [Iquety]*

*在 [... 同样表示可选的部分。*

*对于 些基于服务器 URI, authority 分具有以下形式*

*[user-info^]host[:port】*

*port必 是一个整数。*

*RFC <sup>2396</sup> 标准化URI 文 支持一 基于注册 机制 此时authority 了 一 不同 格式。不 情况并不常 。*

*URI 作 之一是 析标 并将它分 成各 不同 成 分。你可以 以下方法 取它们*

*getScheme getScheneSpecificPart getAuthority getUserlnfo getHost getPort getPath*

getQuery getFragment

URI 类的另一个作用是处理绝对标识符和相对标识符。如果存在一个如下的绝对 URI:

http://docs.mycompany.com/api/java/net/ServerSocket.html

#### 和一个如下的相对 URI:

../../java/net/Socket.html#Socket()

那么可以用它们组合出一个绝对 URI:

http://docs.mycompany.com/api/java/net/Socket.html#Socket()

这个过程称为解析相对 URL。

与此相反的过程称为相对化 (relativization)。例如, 假设有一个基本 URI:

http://docs.mycompany.com/api

和另一个 URI:

http://docs.mycompany.com/api/java/lang/String.html

那么相对化之后的 URI 就是:

java/lang/String.html

URI 类同时支持以下两个操作:

relative = base.relativize(combined);
combined = base.resolve(relative);

#### 4.3.2 使用 URLConnection 获取信息

如果想从某个 Web 资源获取更多信息,那么应该使用 URLConnection 类,通过它能够得到比基本的 URL 类更多的控制功能。

当操作一个 URLConnection 对象时,必须像下面这样非常小心地安排操作步骤:

1. 调用 URL 类中的 openConnection 方法获得 URLConnection 对象:

URLConnection connection = url.openConnection();

2. 使用以下方法来设置各种请求属性:

setDoInput setIoOutput setIfModifiedSince setUseCaches setAllowUserInteraction setRequestProperty setConnectTimeout setReadTimeout

我们将在本节的稍后部分以及 API 说明中讨论这些方法。

3. 调用 connect 方法连接远程资源:

connection.connect();

除了与服务器建立套接字连接外,该方法还可用于向服务器查询头信息 (header information)。

4. 与服务器建立连接后,你可以查询头信息。getHeaderFieldKey 和 getHeaderField 这两个方法枚举了消息头的所有字段。getHeaderFields 方法返回一个包含了消息头中所有字段的标准 Map 对象。为了方便使用,以下方法可以查询各标准字段:

getContentType getContentLength getContentEncoding getDate getExpiration getLastModified

- 5. 最后,访问资源数据。使用 getInputStream 方法获取一个输入流用以读取信息(这个输入流与 URL 类中的 openStream 方法所返回的流相同)。另一个方法 getContent 在实际操作中并不是很有用。由标准内容类型(比如 text/plain 和 image/gif)所返回的对象需要使用com.sun 层次结构中的类来进行处理。也可以注册自己的内容处理器,但是在本书中我们不讨论这项技术。
- 警告: 一些程序员在使用 URLConnection 类的过程中形成了错误的观念,他们认为 URLConnection 类中的 getInputStream 和 getOutputStream 方法与 Socket 类中的这些方法相似,但是这种想法并不十分正确。URLConnection 类具有很多表象之下的神奇功能,尤其在处理请求和响应消息头时。正因为如此,严格遵循建立连接的每个步骤显得非常重要。

下面将详细介绍一下 URLConnection 类中的一些方法。有几个方法可以在与服务器建立连接之前设置连接属性,其中最重要的是 setDoInput 和 setDoOutput。在默认情况下,建立的连接只产生从服务器读取信息的输入流,并不产生任何执行写操作的输出流。如果想获得输出流(例如,用于向一个 Web 服务器提交数据),那么需要调用:

connection.setDoOutput(true);

接下来,也许想设置某些请求头 (request header)。请求头是与请求命令一起被发送到服务器的。例如:

GET www.server.com/index.html HTTP/1.0

Referer: http://www.somewhere.com/links.html

Proxy-Connection: Keep-Alive

User-Agent: Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.4)

Host: www.server.com

Accept: text/html, image/gif, image/jpeg, image/png, \*/\*

Accept-Language: en

Accept-Charset: iso-8859-1,\*,utf-8 Cookie: orangemilano=192218887821987

setIfModifiedSince 方法用于告诉连接,你只对自某个特定日期以来被修改过的数据感兴趣。最后我们再介绍一个统揽全局的方法: setRequestProperty。它可以用来设置对特定协议起作用的任何"名-值(name/value)对"。关于 HTTP 请求头的格式,请参见 RFC 2616,