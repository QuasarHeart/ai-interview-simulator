其中的某些参数没有很好地建档,它们通常在程序员之间口口相传。例如,如果你想访问一个有密码保护的 Web 页,那么就必须按如下步骤操作:

1. 将用户名、冒号和密码以字符串形式连接在一起。

String input = username + ":" + password;

2. 计算上一步骤所得字符串的 Base64 编码。(Base64 编码用于将字节序列编码成可打印的 ASCII 字符序列。)

Base64.Encoder encoder = Base64.getEncoder();
String encoding = encoder.encodeToString(input.getBytes(StandardCharsets.UTF 8));

- 3. 用 "Authorization" 这个名字和 "Basic"+encoding 的值调用 setRequestProperty 方法。connection.setRequestProperty("Authorization", "Basic " + encoding);
- 提示: 我们上面介绍的是如何访问一个有密码保护的 Web 页。如果想要通过 FTP 访问一个有密码保护的文件,则需要采用一种完全不同的方法,即构建如下格式的 URL:

ftp://username:password@ftp.yourserver.com/pub/file.txt

一旦调用了 connect 方法,就可以查询响应头信息了。首先,我们将介绍如何枚举所有响应头的字段。似乎是为了展示自己的个性,该类的实现者引入了另一种迭代协议。调用如下方法:

String key = connection.getHeaderFieldKey(n);

可以获得响应头的第 n 个键,其中 n 从 1 开始!如果 n 为 0 或大于消息头的字段总数,该方法将返回 null 值。没有哪个方法可以返回字段的数量,必须反复调用 getHeaderFieldKey 方法直到返回 null 为止。同样地,调用以下方法:

String value = connection.getHeaderField(n);

可以得到第n个值。

getHeaderFields 方法可以返回一个封装了响应头字段的 Map 对象。

Map<String,List<String>> headerFields = connection.getHeaderFields();

下面是一组来自典型的 HTTP 请求的响应头字段。

Date: Wed, 27 Aug 2008 00:15:48 GMT

Server: Apache/2.2.2 (Unix)

Last-Modified: Sun, 22 Jun 2008 20:53:38 GMT

Accept-Ranges: bytes Content-Length: 4813 Connection: close Content-Type: text/html

**注释:** 可以用 connection.getHeaderField(0) 或 headerFields.get(null) 获取响应状态行(例如 "HTTP/1.1 200 OK")。

为了简便起见, Java 提供了 6 个方法用以访问最常用的消息头类型的值,并在需要的时候将它们转换成数字类型,这些方法的详细信息请参见表 4-1。返回类型为 long 的方法返回的是从格林尼治时间 1970 年 1 月 1 日开始计算的秒数。

| 键 名              | 方法名                | 返回类型   |
|------------------|--------------------|--------|
| Date             | getDate            | long   |
| Expires          | getExpiration      | lang   |
| Last-Modified    | getLastModified    | long   |
| Content-Length   | getContentLength   | int    |
| Content-Type     | getContentType     | String |
| Content-Encoding | getContentEncoding | String |

表 4-1 用于访问响应头值的简便方法

通过程序清单 4-6 的程序,可以对 URL 连接做一些试验。程序运行起来后,请在命令行中输入一个 URL 以及用户名和密码(可选),例如:

java urlConnection.URLConnectionTest http://www.yourserver.com user password

该程序将输出以下内容:

- 消息头中的所有键和值。
- 表 4-1 中 6 个简便方法的返回值。
- 被请求资源的前 10 行信息。

#### 程序清单 4-6 urlConnection/URLConnectionTest.java

```
package urlConnection;
3 import java.io.*;
4 import java.net.*;
5 import java.nio.charset.*;
6 import java.util.*;
8 /**
   * This program connects to an URL and displays the response header data and the first
* 10 lines of the requested data.
11
* Supply the URL and an optional username and password (for HTTP basic authentication) on
* the command line.
14 * @version 1.12 2018-03-17
15 * @author Cay Horstmann
16 */
17 public class URLConnectionTest
      public static void main(String[] args)
19
20
        try
21
22
            String urlName;
23
           if (args.length > 0) urlName = args[0];
```

```
else urlName = "http://horstmann.com";
25
26
             var url = new URL(urlName);
27
            URLConnection connection = url.openConnection();
28
29
            // set username, password if specified on command line
38
31
            if (args.length > 2)
32
33
               String username = args[1];
34
               String password = args[2];
35
                String input = username + ":" + password;
36
                Base64.Encoder encoder = Base64.getEncoder();
37
                String encoding = encoder.encodeToString(input.getBytes(StandardCharsets.UTF 8));
38
                connection.setRequestProperty("Authorization", "Basic " + encoding);
39
40
41
             connection.connect();
47
43
             // print header fields
44
45
             Map<String, List<String>> headers = connection.getHeaderFields();
46
             for (Map.Entry<String, List<String>> entry : headers.entrySet())
47
48
                String key = entry.getKey();
49
                for (String value : entry.getValue())
50
51
                   System.out.println(key + ": " + value);
52
53
             // print convenience functions
55
             System.out.println("----");
             System.out.println("getContentType: " + connection.getContentType());
57
             System.out.println("getContentLength: " + connection.getContentLength());
58
             System.out.println("getContentEncoding: " + connection.getContentEncoding());
59
             System.out.println("getDate: " + connection.getDate());
68
             System.out.println("getExpiration: " + connection.getExpiration());
61
             System.out.println("getLastModifed: " + connection.getLastModified());
             System.out.println("-----");
63
64
             String encoding = connection.getContentEncoding();
             if (encoding == null) encoding = "UTF-8";
66
             try (var in = new Scanner(connection.getInputStream(), encoding))
67
                // print first ten lines of contents
69
                for (int n = 1; in.hasNextLine() && n \le 10; n++)
71
                   System.out.println(in.nextLine());
72
                if (in.hasNextLine()) System.out.println(". . .");
             7
74
75
          catch (IOException e)
76
77
78
             e.printStackTrace();
```

```
79 ]
80 }
81 }
```

#### API java.net.URL

- InputStream openStream()
   打开一个用于读取资源数据的输入流。
- URLConnection openConnection()
   返回一个 URLConnection 对象,该对象负责管理与资源之间的连接。

#### API java.net.URLConnection

- void setDoInput(boolean doInput)
- boolean getDoInput()
   如果 doInput 为 true,那么用户可以接收来自该 URLConnection 的输入。
- void setDoOutput(boolean doOutput)
- boolean getDoOutput()
   如果 doOutput 为 true,那么用户可以将输出发送到该 URLConnection。
- void setIfModifiedSince(long time)
- long getIfModifiedSince()

属性 ifModifiedSince 用于配置该 URLConnection 对象,使它只获取那些自从某个给定时间以来被修改过的数据。调用方法时需要传入的 time 参数指的是从格林尼治时间 1970 年 1 月 1 日午夜开始计算的秒数。

- void setConnectTimeout(int timeout) 5.0
- int getConnectTimeout() 5.0
   设置或得到连接超时时限(单位:毫秒)。如果在连接建立之前就已经达到了超时的时限,那么相关联的输入流的 connect 方法就会抛出一个 SocketTimeoutException 异常。
- void setReadTimeout(int timeout) 5.0
- int getReadTimeout() 5.0

设置读取数据的超时时限(单位:毫秒)。如果在一个读操作成功之前就已经达到了超时的时限,那么 read 方法就会抛出一个 SocketTimeoutException 异常。

- void setRequestProperty(String key, String value)
   设置请求头的一个字段。
- Map<String,List<String>> getRequestProperties() 1.4
   返回请求头属性的一个映射表。相同的键对应的所有值被放置在同一个列表中。
- void connect()连接远程资源并获取响应头信息。
- Map<String,List<String>> getHeaderFields() 1.4

返回响应头的一个映射表。相同的键对应的所有值被放置在同一个列表中。

- String getHeaderFieldKey(int n)
   得到响应头第 n 个字段的键。如果 n 小于或等于 0 或大于响应头字段的总数,则该方 法返回 null 值。
- String getHeaderField(int n)
   得到响应头第 n 个字段的值。如果 n 小于或等于 0 或大于响应头字段的总数,则该方法返回 null 值。
- int getContentLength()
   如果内容长度可获得,则返回该长度值,否则返回-1。
- String getContentType()
   获取内容的类型,比如 text/plain 或 image/gif。
- String getContentEncoding()
   获取内容的编码机制,比如 gzip。这个值不太常用,因为默认的 identity 编码机制并不是用 Content-Encoding 头来设定的。
- long getDate()
- long getExpiration()
- long getLastModifed()
   获取创建日期、过期日以及最后一次被修改的日期。这些日期指的是从格林尼治时间 1970年1月1日午夜开始计算的秒数。
- InputStream getInputStream()
- OutputStream getOutputStream()返回从资源读取信息或向资源写入信息的流。
- Object getContent()
   选择适当的内容处理器,以便读取资源数据并将它转换成对象。该方法对于读取诸如 text/plain或 image/gif 之类的标准内容类型并没有什么用处,除非你安装了自己的 内容处理器。

#### 4.3.3 提交表单数据

在上一节中,我们介绍了如何从 Web 服务器读取数据。现在,我们将介绍如何让程序再将数据反馈回 Web 服务器和那些被 Web 服务器调用的程序。

为了将信息从 Web 浏览器发送到 Web 服务器,用户需要填写一个类似图 4-7 所示的表单。 当用户点击提交按钮时,文本框中的文本以及复选框、单选按钮和其他输入元素的设定 值都被发回 Web 服务器。然后 Web 服务器调用程序对用户的输入进行处理。

有许多技术可以让 Web 服务器实现对程序的调用。其中最广为人知的是 Java Servlet、JavaServer Face、微软的 ASP (Active Server Pages, 动态服务器主页) 以及 CGI (Common Gateway Interface, 通用网关接口) 脚本。

*服务器端程序 于处理表单数据并 成另一个HTML 会 Web服务器发回 浏 器 个操作过程我们在图4-8中做了 明。 回 浏 器 响应 可以包含新 信息 例 如 信息检 序中 响应 或 只是一个 。之后 Web浏 器将显 响应 。*

*我们不会在本书中介 应 如何实 服务器 序 是将侧 点放在如何 写客户 序并使之与已有 服务器端程序进行交互。*

*当 单数据 发 到Web服务器时 数据到底 来 并不 可 是Servlet或 CGI 本 也可 是其他服务器 技术。客户 以标准格式将数据发 Web服务器 Web服务器则 将数据传 具体 序以产 响应。*

*在向Web服务器发 信息时 常有两个命令会 到 GET和POST。*

*在使 GET命令时 只 将参数 在URL的结尾处即可。 URL 格式如下*

*http://host/pathlquery*

*其中 每个参数 具有"名字=值" 形式 些参数之 &<sup>字</sup> <sup>分</sup> <sup>开</sup>。参数 值将 循下 则 使 URL 模式*

*保持字 "A"〜"Z", "a"〜"z", <sup>11</sup> <sup>11</sup>〜"9",以及"〜・'"不变。*

![](_page_6_Figure_1.jpeg)

图 4-8 执行服务器端脚本过程中的数据流

- 用+字符替换所有的空格。
- 将其他所有字符编码为 UTF-8,并将每个字节都编码为 % 后面紧跟一个两位的十六进制数字。

例如,若要发送街道名 San Francisco, CA,可以使用 San+Francisco%2c+CA,因为十六进制数 2c (即十进制数 44)是","的 UTF-8 码值。

这种编码方式使得在任何中间程序中都不会混入空格和其他特殊字符。

例如,就在写作本书的时候,Google Map 网站(www.google.com/maps)可以接受带有两个名为 q 和 h1 参数的查询请求,这两个参数分别表示位置查询和响应中所使用的人类语言。为了得到 1 Market Street, San Franciso 的地图,并且让响应使用德语,只需访问下面的 URL即可:

http://www.google.com/maps?q=1+Market+Street+San+Francisco&hl=de

在浏览器中出现很长的查询字符串很让人郁闷,而且老式的浏览器和代理对在 GET 请求中能够包含的字符数量做出了限制。正因为如此,POST 请求经常用来处理具有大量数据的表单。在 POST 请求中,我们不会在 URL 上附着参数,而是从 URL Connection 中获得输出流,并将名/值对写入该输出流中。我们仍旧需要对这些值进行 URL 编码,并用 & 字符将它们隔开。

下面,我们将详细介绍这个过程。在提交数据给服务器端程序之前,首先需要创建一个 URLConnection 对象。

var url = new URL("http://host/path");
URLConnection connection = url.openConnection();

然后, 调用 setDoOutput 方法建立一个用于输出的连接。

connection.setDoOutput(true);

接着,调用 getOutputStream 方法获得一个流,可以通过这个流向服务器发送数据。如果要向服务器发送文本信息,那么可以非常方便地将流包装在 PrintWriter 对象中。

var out = new PrintWriter(connection.getOutputStream(), StandardCharsets.UTF 8);

现在,可以向服务器发送数据了。

```
out.print(name1 + "=" + URLEncoder.encode(value1, StandardCharsets.UTF_8) + "&");
out.print(name2 + "=" + URLEncoder.encode(value2, StandardCharsets.UTF_8));
```

之后, 关闭输出流:

out.close();

最后,调用 getInputStream 方法读取服务器的响应。

下面我们来实际操作一个例子。地址为 https://tools.usps.com/zip-code-lookup.htm?byad-dress 的网站包含一个用于查找街道地址的邮政编码的表单(见图 4-7)。要想在 Java 程序中使用这个表单,需要知道 POST 请求的 URL 和参数。

你可以通过查看这个表单的 HTML 源码来获取这些信息,但是通常用网络监视器来"窥视"发出的请求会更容易一些。作为其开发工具包的组成部分,大多数浏览器都具有网络监视器。例如,图 4-9 展示了 Firefox 网络监视器向我们的示例网站提交数据时的截屏,从中你可以发现提交对应的 URL 以及参数名和参数值。

![](_page_7_Figure_12.jpeg)

图 4-9 监视表单的提交

在提交表单数据时, HTTP 头包含了内容类型:

Content-Type: application/x-www-form-urlencoded

你还可以以其他格式提交表单。例如,发送用 JavaScript 对象表示法(JSON)表示的数据,将内容类型设置为 application/json。

POST 的头还必须包括内容长度,例如:

Content-Length: 124

程序清单 4-7 用于将 POST 表单数据发送给任何服务器端程序,它将数据放在如下的 .properties 文件:

```
url=https://tools.usps.com/tools/app/ziplookup/zipByAddress
User-Agent=HTTPie/0.9.2
address1=1 Market Street
address2=
city=San Francisco
state=CA
companyName=
```

#### 程序清单 4-7 post/PostTest.java

```
1 package post;
2
3 import java.io.*;
4 import java.net.*:
5 import java.nio.charset.*;
6 import java.nio.file.*;
7 import java.util.*;
9 /**
   * This program demonstrates how to use the URLConnection class for a POST request.
   * @version 1.43 2021-06-17
   * @author Cay Horstmann
12
   */
13
   public class PostTest
15
      public static void main(String[] args) throws IOException
16
17
         String propsFilename = args.length > \theta ? args[\theta] : "post/post.properties";
18
         var props = new Properties();
19
         try (Reader in = Files.newBufferedReader(
28
               Path.of(propsFilename), StandardCharsets.UTF 8))
21
22
            props.load(in);
23
24
         String urlString = props.remove("url").toString();
25
         Object userAgent = props.remove("User-Agent");
26
         Object redirects = props.remove("redirects");
27
         CookieHandler.setDefault(new CookieManager(null, CookiePolicy.ACCEPT ALL));
28
         String result = doPost(new URL(urlString), props,
29
            userAgent == null ? null : userAgent.toString(),
            redirects == null ? -1 : Integer.parseInt(redirects.toString()));
31
         System.out.println(result);
32
33
34
```

```
/**
35
       * Do an HTTP POST.
36
37
       * @param url the URL to post to
       * @param nameValuePairs the query parameters
38
       * @param userAgent the user agent to use, or null for the default user agent
39
       * @param redirects the number of redirects to follow manually, or -1 for automatic
40
41
       * redirects
42
       * @return the data returned from the server
43
      public static String doPost(URL url, Map<Object, Object> nameValuePairs, String userAgent,
44
             int redirects) throws IOException
45
46
         var connection = (HttpURLConnection) url.openConnection();
47
         if (userAgent != null)
48
             connection.setRequestProperty("User-Agent", userAgent);
49
50
         if (redirects >= 0)
51
             connection.setInstanceFollowRedirects(false);
52
53
          connection.setDoOutput(true);
54
55
          try (var out = new PrintWriter(connection.getOutputStream()))
57
             boolean first = true;
             for (Map.Entry<Object, Object> pair : nameValuePairs.entrySet())
             {
60
                if (first) first = false;
                else out.print('&');
62
                String name = pair.getKey().toString();
63
                String value = pair.getValue().toString();
                out.print(name);
65
                out.print('=');
66
                out.print(URLEncoder.encode(value, StandardCharsets.UTF 8));
             }
68
          String encoding = connection.getContentEncoding();
70
          if (encoding == null) encoding = "UTF-8";
71
72
          if (redirects > 0)
73
          1
74
             int responseCode = connection.getResponseCode();
75
             if (responseCode == HttpURLConnection.HTTP MOVED PERM
76
                   || responseCode == HttpURLConnection.HTTP MOVED TEMP
77
                   | responseCode == HttpURLConnection.HTTP SEE OTHER)
             {
79
                String location = connection.getHeaderField("Location");
80
                if (location != null)
                {
82
                   URL base = connection.getURL();
83
                   connection.disconnect();
                   return doPost(new URL(base, location), nameValuePairs, userAgent,
85
                          redirects - 1);
86
                }
87
             }
88
          }
89
```

```
else if (redirects == 0)
98
91
             throw new IOException("Too many redirects");
97
93
94
         var response = new StringBuilder();
95
          try (var in = new Scanner(connection.getInputStream(), encoding))
96
97
             while (in.hasNextLine())
98
99
                response.append(in.nextLine());
                response.append("\n");
181
187
103
          catch (IOException e)
184
105
             InputStream err = connection.getErrorStream();
186
             if (err == null) throw e;
197
             try (var in = new Scanner(err))
198
189
                response.append(in.nextLine());
118
                response.append("\n");
111
             }
112
113
          return response.toString();
115
116
117 }
```

这个程序移除了 url 和 User-Agent 项,并将其他内容都发送到了 doPost 方法。

在 doPost 方法中,我们首先打开连接并设置用户代理。(邮政编码服务在默认的 UserAgent 请求参数包含字符串 Java 时无法工作,这可能是因为邮政局不想为程序自动产生的请求服务。)

调用 setDoOutput(true) 并打开输出流。然后,枚举 Map 对象中的所有键和值。对每一个键 – 值对,我们发送 key、= 字符、value 和 & 分隔符:

```
out.print(key);
out.print('=');
out.print(URLEncoder.encode(value, StandardCharsets.UTF_8));\nif (more pairs) out.print('&');
```

在从写出请求切换到读取任何部分的响应时,都会发生与服务器的实际交互。Content-Length 头被设置为输出的尺寸,而 Content-Type 头被设置为 application/x-www-form-urlencoded,除非指定了不同的内容类型。这些头信息和数据都被发送给服务器,然后,响应头和服务器响应会被读取,并可以被查询。在我们的示例程序中,这种切换发生在对 connection.getContentEncoding()的调用中。

在读取响应过程中会碰到一个问题。如果服务器端出现错误,那么调用 connection. getInputStream() 时就会抛出一个 FileNotFoundException 异常。但是,此时服务器仍然会向浏览器返回一个错误页面(例如,常见的"错误404-找不到该页")。为了捕捉这个错误页.

可以调用 getErrorStream 方法:

InputStream err = connection.getErrorStream();

**注释:** getErrorStream 方法与这个程序中的许多其他方法一样,属于 URLConnection 类的子类 HttpURLConnection。如果要创建以 http://或 https:// 开头的 URL, 那么可以将所产生的连接对象强制转型为 HttpURLConnection。

在将 POST 数据发送给服务器时,服务器端程序产生的响应可能是 redirect:, 后面跟着一个完全不同的 URL, 该 URL 应该被调用以获取实际的信息。服务器之所以可以这么做,是因为这些信息位于他处,或者提供了一个可以作为书签标记的 URL。HttpURLConnection类在大多数情况下可以处理这种重定向。

i 注释:如果 cookie 需要在重定向中从一个站点发送给另一个站点,那么可以像下面这样配置一个全局的 cookie 处理器:

CookieHandler.setDefault(new CookieManager(null, CookiePolicy.ACCEPT\_ALL));

然后, cookie 就可以被正确地包含在重定向请求中了。

尽管重定向通常是自动处理的,但是有些情况下,你需要自己完成重定向。例如,在HTTP和HTTPS之间的自动重定向因为安全原因而不被支持。重定向还会因更细微的原因而失败。例如,早期版本的邮政编码服务就使用了重定向。回忆一下,我们设置了User-Agent请求参数,以便让邮局认为我们不是在通过Java API发送请求。尽管可以在最初的请求中将用户代理设置为其他的字符串,但是这项设置在自动重定向中并没有用到。自动重定向总是会发送包含单词Java的泛化的用户代理字符串。

在这些情况下,可以人工实现重定向。在连接到服务器之前,关闭自动重定向:

connection.setInstanceFollowRedirects(false);

在发送请求之后, 获取响应码:

int responseCode = connection.getResponseCode();

检查它是否是下列值之一:

HttpURLConnection.HTTP\_MOVED\_PERM HttpURLConnection.HTTP\_MOVED\_TEMP HttpURLConnection.HTTP\_SEE\_OTHER

如果是这些值之一,那么获取 Location 响应头,以获得重定向的 URL。然后,断开连接,并创建到新的 URL 的连接:

```
String location = connection.getHeaderField("Location");\nif (location != null)
{
    URL base = connection.getURL();
    connection.disconnect();
    connection = (HttpURLConnection) new URL(base, location).openConnection();
}
```

每当需要从某个现有的 Web 站点查询信息时,该程序所展示的处理技术就会显得很有用。 我们只需找出需要发送的参数,然后从回复信息中剔除 HTML 标签和其他不必要的信息。

#### API java.net.HttpURLConnection 1.0

InputStream getErrorStream()
 返回一个流,通过这个流可以读取 Web 服务器的错误信息。

#### API java.net.URLEncoder 1.0

static String encode(String s, String encoding) 1.4
 采用指定的字符编码模式(推荐使用"UTF-8")对字符串 s 进行编码,并返回它的URL编码形式。在URL编码中, "A"~"Z", "a"~"z", "0"~"9",以及"-", "\_", "."和 "\*"等字符保持不变,空格被编码成 "+",所有其他字符被编码成 "%XY"形式的字节序列,其中 0xXY 为该字节的十六进制数。

#### API java.net.URLDecoder 1.2

static string decode(String s, String encoding) 1.4
 采用指定编码模式对已编码字符串 s 进行解码,并返回结果。

#### 4.4 HTTP 客户端

URLConnection 类是在 HTTP 成为 Web 普适协议之前设计的,它提供了对大量协议的支持,但是它对 HTTP 的支持有些笨重。当做出决定要支持 HTTP/2 时,情况就很清楚了,它最好是提供一个新的客户端接口,而不是对现有 API 做重构。HttpClient 提供了更便捷的 API 和对 HTTP/2 的支持。在 Java 9 和 10 中,其 API 类位于 jdk.incubator.http 包中,使该 API 有机会成为根据用户反馈不断演化的产物。到了 Java 11, HttpClient 位于 java.net.http 包中。

■ 注释: 在使用 Java 9 和 10 时,需要用下面的命令行选项来运行程序:

--add-modules jdk.incubator.httpclient

与 URLConnection 类相比,HTTP 客户端 API 从设计初始就提供了一种更简单的连接到 Web 服务器的机制。

#### 4.4.1 HttpClient 类

HttpClient 对象可以发出请求并接收响应。可以通过下面的调用获取客户端:

HttpClient client = HttpClient.newHttpClient()

或者,如果需要配置客户端,可以使用像下面这样的构建器 API:

HttpClient client = HttpClient.newBuilder()

.followRedirects(HttpClient.Redirect.ALWAYS)

.build();

即,获取一个构建器,调用其方法定制需要待构建的项,然后调用 build 方法来完结构

建过程。这是一种构建不可修改对象的常见模式。

#### 4.4.2 HttpRequest 类和体发布器

还可以遵循构建器模式来定制请求,下面是一个 Get 请求:

```
HttpRequest request = HttpRequest.newBuilder()
   .uri(new URI("http://horstmann.com"))
   .build():
```

URI 是指"统一资源标识符",在使用 HTTP 时,它与 URL 相同。但是,在 Java 中, URL 类确实有一些用来打开到某个 URL 的连接的方法, 而 URI 类只关心语法(模式、主机、 端口、路径、杳询、片段等)。

对于 POST 请求, 需要一个"体发布器" (body publisher), 它会将请求数据转换为要推送 的数据。有针对字符串、字节数组和文件的体发布器。例如,如果请求是 JSON 格式的,那 么只需将 JSON 字符串提供给某个字符串体发布器:

```
HttpRequest request = HttpRequest.newBuilder()
   .uri(new URI(url))
   .header("Content-Type", "application/json")
   .POST(HttpRequest.BodyPublishers.ofString(jsonString))
   .build():
```

遗憾的是,该API不支持对常见内容类型做上面所要求的格式化处理。程序清单 4-8 中 的样例程序提供了用于表单数据和文件上传的体发布器。

Java 16 新添加了一个构建器,用于过滤已有的 HttpRequest 的头。你需要提供该请求, 以及用于接收请求头中的名字和值的函数,该函数会在这些头应该保留时返回 true。例如, 下面的代码会修改内容类型:

```
HttpRequest request2 = HttpRequest.newBuilder(request,
      (name, value) -> !name.equalsIgnoreCase("Content-Type")) // Remove old content type
   .header("Content-Type", "application/xml") // Add new content type
   .build():
```

#### 4.4.3 HttpResponse 接口和体处理器

在发送请求时,必须告诉客户端如何处理响应。如果只是想将体当作字符串处理,那么 就可以像下面这样用 HttpResponse.BodyHandlers.ofString() 来发送请求:

HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

HttpResponse 类是一个泛化接口,它的类型参数表示体的类型。可以直接获取响应体字符串: String bodyString = response.body();

还有其他的响应体处理器,可以将响应作为字节数组或输入流来获取。BodyHandlers. ofFile(filePath)会产生一个处理器,将响应存储到给定的文件中,BodyHandlers.ofFile-Download(directoryPath) 会用 Content-Disposition 头中的文件名将响应存入给定的目录中。最 后,从 BodyHandlers.dicarding()中获得的处理器会直接丢弃响应。

处理响应的内容并不在该 API 的考虑范围内。例如,如果收到了 JSON 数据,那么就需要某个 JSON 库来解析其中的内容。

HttpResponse 对象还会产生状态码与响应头。

int status = response.statusCode();
HttpHeaders responseHeaders = response.headers();

可以将 HttpHeaders 对象转换为一个映射表:

Map<String, List<String>> headerMap = responseHeaders.map();

这个映射表的值是列表,因为在 HTTP中,每个键都可以有多个值。

如果只想要某个特定键的值,并且知道它没有多个值,那么可以调用 firstValue 方法:

Optional<String> lastModified = headerMap.firstValue("Last-Modified");

这样可以得到该响应的值,或者在没有提供该值时,返回空的 Optional 对象。

#### 4.4.4 异步处理

可以异步地处理响应。在构建客户端时,可以提供一个执行器:

ExecutorService executor = Executors.newCachedThreadPool();
HttpClient client = HttpClient.newBuilder().executor(executor).build();

构建一个请求,然后在该客户端上调用 sendAsync 方法,就会收到一个 CompletableFuture <a href="httpResponse<1">httpResponse<1</a>>> 对象,其中 T 是体处理器的类型。需要使用卷 I 第 12 章描述的 Completable-Future API:

```
HttpRequest request = HttpRequest.newBuilder().uri(uri).GET().build();
client.sendAsync(request, HttpResponse.BodyHandlers.ofString())
    thenAccept(response -> . . .);
```

☑ 提示: 为了启用针对 HttpClient 记录日志的功能,需要在 JDK 的 net.properties 文件中添加下面的行:

jdk.httpclient.HttpClient.log=all

除了all,还可以指定一个由逗号分隔的列表,其中包含 headers、requests、content、errors、ssl、trace 和 frames,后面还可以选择跟着:control、:data、:window或:all。中间不要使用任何空格。

然后,将名为 jdk.httpclient.HttpClient 的日志记录器的日志级别设置为 INFO, 例如,在 JDK 的 logging.properties 文件中添加下面的行:

jdk.httpclient.HttpClient.level=INFO

#### 程序清单 4-8 client/HttpClientTest.java

```
1 package client;
```

<sup>2</sup> 

<sup>3</sup> import java.io.\*;

<sup>4</sup> import java.math.\*;

```
5 import java.net.*;
6 import java.nio.charset.*;
7 import java.nio.file.*;
8 import java.util.*;
9
   import java.net.http.*;
   import java.net.http.HttpRequest.*;
11
12
   class MoreBodyPublishers
13
14
      public static BodyPublisher ofFormData(Map<Object, Object> data)
15
16
         boolean first = true;
17
         var builder = new StringBuilder();
18
         for (Map.Entry<Object, Object> entry : data.entrySet())
19
20
             if (first) first = false;
21
             else builder.append("&");
22
             builder.append(URLEncoder.encode(entry.getKey().toString(),
23
                 StandardCharsets.UTF 8));
             builder.append("=");
25
26
             builder.append(URLEncoder.encode(entry.getValue().toString(),
                 StandardCharsets.UTF 8));
27
78
         return BodyPublishers.ofString(builder.toString());
29
30
31
      private static byte[] bytes(String s) { return s.getBytes(StandardCharsets.UTF 8); }
32
33
      public static BodyPublisher ofMimeMultipartData(Map<Object, Object> data, String boundary)
34
            throws IOException
35
36
         var byteArrays = new ArrayList<byte[]>();
37
         byte[] separator = bytes("--" + boundary + "\nContent-Disposition: form-data; name=");
38
         for (Map.Entry<Object, Object> entry : data.entrySet())
39
48
             byteArrays.add(separator);
41
42
            if (entry.getValue() instanceof Path path)
43
44
            {
                String mimeType = Files.probeContentType(path);
45
                byteArrays.add(bytes("\"" + entry.getKey() + "\"; filename=\""
46
                   + path.getFileName() + "\"\nContent-Type: " + mimeType + "\n\n"));
47
                byteArrays.add(Files.readAllBytes(path));
48
            }
49
             else
50
                byteArrays.add(bytes("\"" + entry.getKey() + "\"\n\n" + entry.getValue() + "\n"));
51
52
        byteArrays.add(bytes("--" + boundary + "--"));
53
         return BodyPublishers.ofByteArrays(byteArrays);
54
      }
55
56
      public static BodyPublisher ofSimpleJSON(Map<Object, Object> data)
57
58
59
          var builder = new StringBuilder();
```

```
builder.append("{");
         var first = true;
61
         for (Map.Entry<Object, Object> entry : data.entrySet())
62
63
            if (first) first = false;
64
            else
65
               builder.append(",");
            builder.append(jsonEscape(entry.getKey().toString())).append(": ")
67
                .append(jsonEscape(entry.getValue().toString()));
68
69
         builder.append("}");
78
         return BodyPublishers.ofString(builder.toString());
71
72
73
      private static Map<Character, String> replacements = Map.of('\b', "\\b", '\f', "\\f",
74
          '\n', "\\n", '\r', "\\r", '\t', "\\t", '"', "\\\"", '\\\");
75
76
      private static StringBuilder jsonEscape(String str)
77
78
         var result = new StringBuilder("\"");
79
         for (int i = 0; i < str.length(); i++)
80
81
            char ch = str.charAt(i);
82
            String replacement = replacements.get(ch);
83
            if (replacement == null) result.append(ch);
84
            else result.append(replacement);
85
RE
          result.append("\"");
87
88
          return result;
89
98
91
   public class HttpClientTest
92
93
      public static void main(String[] args)
94
             throws IOException, URISyntaxException, InterruptedException
95
96
          System.setProperty("jdk.httpclient.HttpClient.log", "headers,errors");
97
          String propsFilename = args.length > 0 ? args[0] : "client/post.properties";
98
          Path propsPath = Path.of(propsFilename);
99
          var props = new Properties();
188
101
          try (Reader in = Files.newBufferedReader(propsPath, StandardCharsets.UTF 8))
          {
102
             props.load(in);
183
104
          String urlString = "" + props.remove("url");
105
          String contentType = "" + props.remove("Content-Type");
106
          if (contentType.equals("multipart/form-data"))
107
108
             var generator = new Random():
109
             String boundary = new BigInteger(256, generator).toString();
118
             contentType += ";boundary=" + boundary;
111
             props.replaceAll((k, v) ->
112
                v.toString().startsWith("file://")
113
                   ? propsPath.getParent().resolve(Path.of(v.toString().substring(7)))
114
```

```
: v);
115
116
         String result = doPost(urlString, contentType, props);
117
         System.out.println(result);
118
119
120
      public static String doPost(String url, String contentType, Map<Object, Object> data)
121
             throws IOException, URISyntaxException, InterruptedException
122
      {
123
         HttpClient client = HttpClient.newBuilder()
124
             .followRedirects(HttpClient.Redirect.ALWAYS).build();
125
126
          BodyPublisher publisher = null;
127
          if (contentType.startsWith("multipart/form-data"))
128
129
             String boundary = contentType.substring(contentType.lastIndexOf("=") + 1);
138
             publisher = MoreBodyPublishers.ofMimeMultipartData(data, boundary);
131
132
          else if (contentType.equals("application/x-www-form-urlencoded"))
133
             publisher = MoreBodyPublishers.ofFormData(data);
134
          else
135
136
             contentType = "application/json";
137
             publisher = MoreBodyPublishers.ofSimpleJSON(data);
138
139
149
         HttpRequest request = HttpRequest.newBuilder()
141
             .uri(new URI(url))
             .header("Content-Type", contentType)
143
             .POST(publisher)
144
             .build();
145
          HttpResponse<String> response
146
             = client.send(request, HttpResponse.BodyHandlers.ofString());
147
          return response.body();
148
149
150 }
```

#### API java.net.http.HttpClient

- static HttpClient newHttpClient()
   用默认配置产生一个 HttpClient 对象。
- static HttpClient.Builder newBuilder()
   产生一个用于构建 HttpClient 对象的构建器。
- <T> HttpResponse<T> send(HttpRequest request, HttpResponse.BodyHandler<T> responseBodyHandler)
- <T> CompletableFuture<HttpResponse<T>> sendAsync(HttpRequest request, HttpResponse .BodyHandler <T> responseBodyHandler)

产生一个同步或异步的请求, 并使用给定的处理器来处理响应体。

#### java.net.http.HttpClient.Builder

HttpClient build()

用由当前构建器配置的属性产生一个 HttpClient 对象。

- HttpClient.Builder followRedirects(HttpClient.Redirect policy)
   将重定向策略设置为 HttpClient.Redirect 枚举中的 ALWAYS、NEVER 或 NORMAL 之一(仅 拒绝从 HTTPS 重定向到 HTTP)。
- HttpClient.Builder executor(Executor executor)
   设置用于异步请求的执行器。

#### API java.net.http.HttpRequest

- HttpRequest.Builder newBuilder()
   产生一个用于构建 HttpRequest 对象的构建器。
- HttpRequest.Builder newBuilder(HttpRequest request, BiPredicate<String, String>filter) 16 返回一个构建器,它会用与所提供的请求相同的属性构建一个请求,并且只保留过滤器接收的头信息。

#### API java.net.http.HttpRequest.Builder

- HttpRequest build()
   用由当前构建器配置的属性产生一个 HttpRequest 对象。
- HttpRequest.Builder uri(URI uri)
   为当前请求设置 URI。
- HttpRequest.Builder header(String name, String value)
   为当前请求设置请求头。
- HttpRequest.Builder GET()
- HttpRequest.Builder DELETE()
- HttpRequest.Builder POST(HttpRequest.BodyPublisher bodyPublisher)
- HttpRequest.Builder PUT(HttpRequest.BodyPublisher bodyPublisher)
   为当前请求设置请求方法和请求体。

#### java.net.http.HttpResponse<T>

- T body() 产生当前响应的体。
- int statusCode()产生当前响应的状态码。
- HttpHeaders headers()
   产生响应头。

#### API java.net.http.HttpHeaders

Map<String,List<String>> map()
 产生由这些头构成的映射表。

Optional<String> firstValue(String name)
 在头中具有给定名称的第一个值,如果存在的话。

#### 4.5 发送 E-mail

过去,编写程序通过创建到邮件服务器上 SMTP 专用的端口 25 来发送邮件是一件很简单的事。简单邮件传输协议用于描述 E-mail 消息的格式。一旦连接到服务器,就可以发送一个邮件报头(采用 SMTP 格式,该格式很容易生成)。紧随其后的是邮件消息。

以下是操作的详细过程。

1. 打开一个到达主机的套接字:

var s = new Socket("mail.yourserver.com", 25); // 25 is SMTP
var out = new PrintWriter(s.getOutputStream(), StandardCharsets.UTF 8);

2. 发送以下信息到打印流:

HELO sending host

MAIL FROM: sender e-mail address RCPT TO: recipient e-mail address

DATA

Subject: subject (blank line) mail message (any number of lines)

QUIT

SMTP 规范 (RFC 821) 规定,每一行都要以 \r 再紧跟一个 \n 来结尾。

SMTP 曾经总是例行公事般地路由任何人的 E-mail。但是,在垃圾邮件泛滥的今天,许多服务器都内置了检查功能,并且只接受来自授信用户或授信 IP 地址范围的请求。其中,认证通常是通过安全套接字连接来实现的。

实现人工认证模式的代码非常冗长乏味,因此,我们将展示如何利用 JavaMail API 在 Java 程序中发送 E-mail。

可以从 www.oracle.com/technetwork/java/javamail 处下载 JavaMail, 然后将它解压到硬盘上的某处。

如果要使用 JavaMail,则需要设置一些和邮件服务器相关的属性。例如,在使用 GMail 时,需要设置:

mail.transport.protocol=smtps
mail.smtps.auth=true
mail.smtps.host=smtp.qmail.com

mail.smtps.user=accountname@gmail.com

我们的示例程序是从一个属性文件中读取这些属性值的。

出于安全的原因, 我们没有将密码放在属性文件中, 而是提示用户需要输入。

首先要读入属性文件,然后像下面这样获取一个邮件会话:

Session mailSession = Session.getDefaultInstance(props);

#### 接着,用恰当的发送者、接收者、主题和消息文本来创建消息:

```
var message = new MimeMessage(mailSession);
message.setFrom(new InternetAddress(from));
message.addRecipient(RecipientType.TO, new InternetAddress(to));
message.setSubject(subject);
message.setText(builder.toString());
```

#### 然后将消息发送走:

```
Transport tr = mailSession.getTransport();
tr.connect(null, password);
tr.sendMessage(message, message.getAllRecipients());
tr.close();
```

程序清单 4-9 中的程序是从具有下面这种格式的文本文件中读取消息的:

Sender Recipient Subject Message text (any number of lines)

要运行该程序,需要从 https://javaee.github.io/javamail下载 JavaMail 的实现,还需要 Java 激活框架 (Java Activation Framework) 的 JAR 文件,可以从 https://www.oracle.com/java/technologies/downloads.html 处获得,或者可以在 Maven Central 中搜索。然后运行:

java -classpath .: javax.mail.jar:activation-1.1.1.jar path/to/message.txt

到撰写本章时为止, GMail 还不会检查信息的真实性,即你可以输入任何你喜欢的发送者。(当你下一次收到来自 president@whitehouse.gov 的 E-mail 消息邀请你盛装出席白宫南草坪的活动时,请牢记这一点,谨防上当。)

√ 提示: 如果你搞不清楚为什么你的邮件连接无法正常工作,那么可以调用:
mailSession.setDebug(true);

并检查消息。而且, JavaMail API FAQ 也有些挺有用的调试提示。

#### 程序清单 4-9 mail/MailTest.java

```
package mail;
\nimport java.io.*;
\nimport java.nio.charset.*;
\nimport java.nio.file.*;
\nimport java.util.*;
\nimport javax.mail.*;
\nimport javax.mail.internet.*;
\nimport javax.mail.internet.MimeMessage.RecipientType;

/**

* This program shows how to use JavaMail to send mail messages.

* @author Cay Horstmann

* @version 1.02 2021-06-17
```

```
228
```

```
15
   public class MailTest
16
17
      public static void main(String[] args) throws MessagingException, IOException
18
19
         var props = new Properties();
28
         try (Reader in = Files.newBufferedReader(Path.of("mail",
21
                "mail.properties"), StandardCharsets.UTF 8))
22
23
            props.load(in);
24
25
         List<String> lines = Files.readAllLines(Path.of(args[0]), StandardCharsets.UTF_8);
26
27
         String from = lines.get(0);
28
         String to = lines.get(1);
29
30
         String subject = lines.get(2);
31
         var builder = new StringBuilder();
32
         for (int i = 3; i < lines.size(); i++)
33
34
             builder.append(lines.get(i));
35
             builder.append("\n");
36
37
38
          Console console = System.console();
39
          var password = new String(console.readPassword("Password: "));
48
41
          Session mailSession = Session.getDefaultInstance(props);
42
          // mailSession.setDebug(true);
43
          var message = new MimeMessage(mailSession);
          message.setFrom(new InternetAddress(from));
45
          message.addRecipient(RecipientType.TO, new InternetAddress(to));
46
47
          message.setSubject(subject);
          message.setText(builder.toString());
48
          Transport tr = mailSession.getTransport();
49
          try
50
51
             tr.connect(null, password);
52
             tr.sendMessage(message, message.getAllRecipients());
54
          finally
55
             tr.close();
57
58
59
   }
68
```

在本章中, 你已经看到了如何用 Java 编写网络客户端和服务器, 以及如何从 Web 服务器上获取数据。下一章将讨论数据库连接, 你将会学习如何通过使用 JDBC API 来实现用 Java 操作关系型数据库。

## *5 数据库*

- *JDBC*
- *▲ 构化査询语言*
- *JDBC配置*
- *▲使 JDBC <sup>句</sup>*
- *▲执 査 操作*

- *▲可滚动和可更新 果*
- *▲*
- *▲元数据*
- *▲事务*
- *Web与企业应 <sup>中</sup> <sup>接</sup>*

*<sup>1996</sup><sup>年</sup> Sun公司发布了 1版的Java数据库 <sup>接</sup> JDBC API,<sup>使</sup> 人员可以 个API接口 接到数据库 并使 构化査 即SQL 完成对数据库 査找与更 <sup>新</sup>。 SQL 常发 <sup>为</sup>"sequel" 它是数据库 <sup>业</sup> 标准。 JDBC 此成为Java 库中 最常使用的API之一。*

*JDBC 本已更新 数次。在本书出 <sup>之</sup> 最新 JDBC 4.3<sup>也</sup> 囊括到了 Java 9<sup>中</sup>。 在本 中 我们将阐述JDBC幕后 关 思想 并将介 或 是复习 一下SQL Structured Query Language, 构化查询语言 它是关 数据库 业 标准。我们 将提供 够的细节 使你可以将JDBC 人常 场景中。*

*注 根据<sup>O</sup> racle 声明 JDBC是一个注册了商标 术 并 Java Database Connectivity 字母 写。对它 命名体 了对ODBC 敬 后 是微 开创 标准數据库API,并因此 并入了 SQL标准中。*

# *5.1 JDBC*

*从一开始 Java技术开发人员就意 到了 Java在数据库应 方 巨大潜力。从<sup>1995</sup> 年开始 他们就 力于扩展Java标准 库 使之可以 SQL访问数据库。他们最初希望 扩展Java,就可以 人们" " Java 与任何数据库 信。但是 他们很快发 是一 无法完成 任务 因为.业 存在 多不同 数据库 且它们所使 协 也各不 同。尽 很多数据库供应商都表示支持Java提供一套数据库 标准 协 但是每 一家企业 希望Java 己 协 。*

*所有 数据库供应商和工具开发商 为 如果Java 够为SQL 提供一套 " " Java API,同时提供一个 动 器 以允许第三方 动 序可以 接到 定 数据 库 它就会显得 常有 。 样 数据库供应商就可以提供 己 动 序 将其插入到 动 器中。 将成为一 向 动 器注册 三方 动 序 单机制。*

这种接口组织方式遵循了微软公司非常成功的 ODBC 模式, ODBC 为 C 语言访问数据库提供了一套编程接口。JDBC 和 ODBC 都基于同一个思想:根据 API 编写的程序都可以与驱动管理器进行通信,而驱动管理器则通过驱动程序与实际的数据库进行通信。

所有这些都意味着 JDBC API 是大部分程序员不得不使用的接口。

#### 5.1.1 JDBC 驱动程序类型

JDBC 规范将驱动程序归结为以下几类:

- 第1类驱动程序将JDBC翻译成ODBC,然后使用ODBC驱动程序与数据库进行通信。较早版本的Java包含了一个这样的驱动程序:JDBC/ODBC桥,不过在使用这个桥接器之前需要对ODBC进行相应的部署和正确的设置。在JDBC面世之初,桥接器可以方便地用于测试,却不太适用于产品的开发。现在,有很多更好的驱动程序可用,所以JDK已经不再提供JDBC/ODBC桥了。
- 第2类驱动程序是由部分Java程序和部分本地代码组成的,用于与数据库的客户端API进行通信。在使用这种驱动程序之前,客户端不仅需要安装Java类库,还需要安装一些与平台相关的代码。
- 第3类驱动程序是纯 Java 客户端类库,它使用一种与具体数据库无关的协议将数据库 请求发送给服务器构件,然后该构件再将数据库请求翻译成数据库相关的协议。这简 化了部署,因为平台相关的代码只位于服务器端。
- 第 4 类驱动程序是纯 Java 类库,它将 JDBC 请求直接翻译成数据库相关的协议。
- 注释: JDBC 规范可以在 https://jcp.org/aboutJava/communityprocess/mrel/jsr221/index3.
   html 处获得。

大部分数据库供应商都为他们的产品提供第3类或第4类驱动程序。与数据库供应商提供的驱动程序相比,许多第三方公司专门开发了很多更符合标准的产品,它们支持更多的平台、运行性能也更佳,某些情况下甚至具有更高的可靠性。

总之, JDBC 最终是为了实现以下目标:

- 通过使用标准的 SQL 语句, 甚至是专门的 SQL 扩展,程序员就可以利用 Java 语言开发访问数据库的应用,同时还依旧遵守 Java 语言的相关约定。
- 数据库供应商和数据库工具开发商可以提供底层的驱动程序。因此,他们可以优化各 自数据库产品的驱动程序。
- 直 注释: 也许你会问为什么 Java 没有采用 ODBC 模型, 下面就是在 1996 年举行的 JavaOne 研讨会上给出的说法:
  - ODBC 很难学会。
  - ODBC 中有几个命令需要配置很多复杂的选项,而在 Java 编程语言中所采用的风格是要让方法简单而直观,但数量巨大。

- *• ODBC<sup>依</sup> <sup>于</sup>void\*<sup>指</sup> 和其他<sup>C</sup> <sup>性</sup> 而这些 <sup>性</sup>Java 并不具备。*
- *与 Java 决方案 比 基于ODBC 决方案天 就 乏安全性 且 于 部署。*

# *5.1.2 JDBC 典型 <sup>法</sup>*

*在传 客户 /服务器模型中 常是在服务器 数据库 在客户 安 富 GUI 序 参 图5-1 。在此模型中 JDBC 动 序应 在客户 。*

*但是 如今三层模型更加常 。在 三层应 模型中 客户 不 接 数 据库 是 服务器上 中 件层 中 件层完成数据库査 操作。这种 三层模型有以下优点 它将可 化 位于客户 从业务逻辑 位于中 层 和原始数据 位于数据库 中分 出来。 因此 我们可以从不同 客户 如*

![](_page_24_Figure_7.jpeg)

*图5-1<sup>传</sup> 客户 /服务器应*

*Java桌 应 、浏 器或 动App,来 同 数据和 同 业务 则。*

*客户 和中 层之 信在典型情况下是 HTTP来实现的。JDBC 中 层 和后台数据库之 信 图5-2展 了 信模型 基本架构。*

![](_page_24_Figure_11.jpeg)

*图5-2三层 <sup>构</sup> <sup>应</sup>*

## *5.2 构化查*

*SQL是对所有 代关 型数据库 关 命令 JDBC则使得我们可以 SQL与数据库 信。桌 数据库 常 有一个图形 户 户可以 接操作数据。但是 基于服务器 数据库只 使 SQL进行访问。*

*我们可以将JDBC包 作是一个 于将SQL 句传 数据库 应 接口 API <sup>o</sup> 在本 中 我们将 单介 一下SQL。如果之前没有接触过SQL,你会发现这些介 是*

远不够的,你可以参阅关于 SQL 的其他著作。我们推荐 Alan Beaulieu 所著的 Learning SQL (2009 年由 OReilly 出版社出版),或者还可以参考在线图书 Learn SQL The Hard Way,该书可在 http://sql.learncodethehardway.org 处获得。

可以将数据库想象成一组由行和列构成的具名表,其中每一列都有列名(column name),而每一行则包含了一个相关的数据集。

作为本书的数据库实例,我们将使用一组数据库表来描述一组经典的计算机著作(请参见表 5-1~表 5-4)。

表 5-1 Authors 表

| Author_ID | Name      | Fname        |
|-----------|-----------|--------------|
| ALEX      | Alexander | Christopher  |
| BR00      | Brooks    | Frederick P. |
| ***       | ÷         | 1.11         |

表 5-2 Books 表

| Title                                              | ISBN          | Publisher_ID | Price |
|----------------------------------------------------|---------------|--------------|-------|
| A Guide to the SQL Standard                        | 0-201-96426-0 | 0201         | 47.95 |
| A Pattern Language: Towns, Buildings, Construction | 0-19-501919-9 | 019          | 65.00 |
|                                                    | ***           |              | 6.4%  |

表 5-3 BooksAuthors 表

| ISBN          | Author_ID | Seq_No |
|---------------|-----------|--------|
| 0-201-96426-0 | DATE      | 1      |
| 0-201-96426-0 | DARW      | 2      |
| 0-19-501919-9 | ALEX      | 1      |
| ***           | ***       | ***    |

表 5-4 Publishers 表

| Publisher_ID | Name              | URL           |
|--------------|-------------------|---------------|
| 0201         | Addison-Wesley    | www.aw-bc.com |
| 0407         | John Wiley & Sons | www.wiley.com |
| ***          |                   |               |

图 5-3 显示的是一个 Books 表的视图,而图 5-4 显示了对 Books 表和 Publishers 表执行连接操作后的结果。Books 表和 Publishers 表都包含了一个表示出版社的 ID 字段。当我们利用出版社编号对这两个表进行连接操作时,我们就得到了由连接后的表格的值所组成的查询结果。结果中的每一行都包含了图书的信息、出版社名称及其 Web 页的 URL 地址。注意,有的出版社名称和 URL 地址会重复出现在数行中,因为这些行都对应于同一个出版社。

| 5 | 图 品面目的图 8 · 成公公                                             | 古本本           | 平回。          |        |
|---|-------------------------------------------------------------|---------------|--------------|--------|
|   | Title                                                       | ISBN          | Publisher ID | Price  |
|   | JNIX System Administration Handbook                         | 0-13-020601-6 | 013          | 58.00  |
|   | The C Programming Language                                  | 0-13-110362-8 | 013          | 42.00  |
|   | A Pattern Language: Towns, Buildings, Construction          | 0-19-501919-9 | 019          | 65.00  |
|   | introduction to Automata Theory, Languages, and Computation | 0-201-44124-1 | 0201         | 105.00 |
|   | Design Patterns                                             | 0-201-63361-2 | 0201         | 54.99  |
|   | The C++ Programming Language                                | 0-201-70073-5 | 0201         | 64.99  |
|   | The Mythical Man-Month                                      | 0-201-83595-9 | 0201         | 29.95  |
|   | Computer Graphics: Principles and Practice                  | 0-201-84840-6 | 0201         | 79.99  |
|   | The Art of Computer Programming vol. 1                      | 0-201-89683-4 | 0201         | 59.99  |
|   | The Art of Computer Programming vol. 2                      | 0-201-89684-2 | 0201         | 59.99  |
|   | The Art of Computer Programming vol. 3                      | 0-201-89685-0 | 0201         | 59.99  |
|   | A Guide to the SQL Standard                                 | 0-201-96426-0 | 0201         | 47.95  |
|   | Introduction to Algorithms                                  | 0-262-03293-7 | 0262         | 80.00  |
|   | Applied Cryptography                                        | 0-471-11709-9 | 0471         | 60.00  |
|   | javaScript: The Definitive Guide                            | 0-596-00048-0 | 0596         | 44.95  |
|   | The Cathedral and the Bazaar                                | 0-596-00108-8 | 0596         | 16.95  |
|   | The Soul of a New Machine                                   | 0-679-60261-5 | 0679         | 18.95  |
|   | The Codebreakers                                            | 0-684-83130-9 | 07434        | 70.00  |
|   | Cuckoo's Egg                                                | 0-7434-1146-3 | 07434        | 13.95  |
|   | The UNIX Hater's Handbook                                   | 1-56884-203-1 | 0471         | 16.95  |

*图5-3包含图书信息 <sup>例</sup> <sup>格</sup>*

|                                                                   | Marie Control              |                               |                                |                    |                |                        |             |   |   |   |
|-------------------------------------------------------------------|----------------------------|-------------------------------|--------------------------------|--------------------|----------------|------------------------|-------------|---|---|---|
| 8                                                                 | 7 % 6                      | 0000                          | NO 5 8                         | for the            | Z,             |                        |             |   |   |   |
| <b>M</b> F                                                        | O X S                      | 000                           | D - 102 12 5                   | 242                | 中國             | <b>3</b> 5             | <b>P O</b>  |   |   |   |
|                                                                   |                            | Yitle                         |                                | Publisher_IC       | Price          | Name                   | URL         |   |   | - |
|                                                                   |                            | stration Handbook             |                                | 013                | 68.00          | Prentice H             |             |   |   |   |
|                                                                   | C Programming              |                               |                                | 013                | 42.00          | Prentice H             |             |   |   |   |
|                                                                   |                            | Towns, Buildings, C           |                                | 019                | 65.00          | Oxford Uni             |             |   |   |   |
|                                                                   |                            | mata Theory, Langu            | ages, and Computatio           |                    | 105.00         | Addison-W              |             |   |   |   |
|                                                                   | gn Patterns                |                               |                                | 0201               | 54.99          | Addison-W              |             |   |   |   |
|                                                                   | C++ Programm               |                               |                                | 0201               | 64 99<br>29 95 | Addison-W<br>Addison-W |             |   |   |   |
|                                                                   | Mythical Man Mo            | Principles and Pract          | **                             | 0201               | 79.99          | Addison-W              |             |   |   |   |
|                                                                   |                            | Programming vol. 1            |                                | 0201               | 59.99          | Addison-W              |             |   |   |   |
|                                                                   |                            | Programming vol. 2            |                                | 0201               | 59.99          | Addison-W              |             |   |   |   |
|                                                                   |                            | Programming vol. 3            |                                | 0201               | 59.99          | Addison-W              |             |   |   |   |
|                                                                   |                            |                               |                                |                    |                |                        | MARKS 72.00 |   |   |   |
| M Boo                                                             | of                         | TO Pub                        | lishers                        |                    |                |                        | www.aw      |   |   |   |
| Boo                                                               | oks<br>s<br>N<br>olisher_D | 15 Pub                        | lishers                        |                    |                |                        |             |   |   |   |
| Book Train                                                        | of oks                     | TO Pub                        | lishers<br>lisher_id           |                    |                |                        | W. W.       |   |   |   |
| M Boo                                                             | oks<br>s<br>N<br>olisher_D | TO Pub<br>Pub<br>Nar          | lishers                        | Name               | URL            |                        | were an     |   |   |   |
| Book Title Pub Price                                              | of oks                     | ## Publisher_ID               | lishers lisher_ld ne           | Name               | LIRL           |                        | were an     |   |   |   |
| Book Tick Tick Tick Tick Tick Tick Tick Tic                       | of oks                     | TO Pub                        | lishers lisher_ld ne           |                    |                | •                      | were an     |   |   |   |
| Book Ticle V ISB Pub Price Idea Idea Idea Idea Idea Idea Idea Ide | of oks                     | 35 = Duble Publisher_O  Books | Ishers Isher_Id ne Price Books | Name<br>Publishers | LIRL.          |                        | west Ja     |   |   |   |
| Book Table Published Price                                        | of oks                     | ## Publisher_ID               | lishers lisher_ld ne           | Name               | LIRL           |                        |             |   |   |   |
| Title VISB Pub Pric Visible\nunction                              | of oks                     | 35 = Duble Publisher_O  Books | Ishers Isher_Id ne Price Books | Name<br>Publishers | LIRL.          |                        |             |   | ū |   |
| M Boo                                                             | of oks                     | 35 = Duble Publisher_O  Books | Ishers Isher_Id ne Price Books | Name<br>Publishers | LIRL.          |                        | 0           |   |   |   |
| Title VISB Pub Pric Visible\nunction                              | of oks                     | 35 = Duble Publisher_O  Books | Ishers Isher_Id ne Price Books | Name<br>Publishers | LIRL.          |                        |             | T | a |   |

*<sup>图</sup>S4对两个表进行连接操作*

*对 格 接操作 好处是 够 免在数据库 中出 不必 复数据。例如 有一 比 数据库 是在Books 中设置出版社名 和URL地址字段。但是 样一来, 数据库本 査 果 将出 多 复数据。如果出 Web地址发 了改变 就 更新所有 复数据。显然 在一定 度上很容易导 。在关 模型中 我们将数 据分布到多个 中 使得所有信息 不会出 不必 复。例如 每个出 URL地址 只在出 巾出 一次。如果 将此信息与其他信息 合 我们只 对 接操作。*

*在上 两幅图中 可以 到一个 于查 和 接 图形工具。 多数据库提供商 具*

有相应的工具,通过连接列名和在表单中填入信息,让用户能够以某种简单的形式来表示其各种查询。这种工具通常称为实例查询(Query by Example, QBE)工具。而使用 SQL 的查询则是利用 SQL 语法以文本方式编写的。例如,

SELECT Books.Title, Books.Publisher\_Id, Books.Price, Publishers.Name, Publishers.URL FROM Books, Publishers
WHERE Books.Publisher Id = Publishers.Publisher Id

在本节的余下部分中,我们将介绍如何编写这样的查询语句。如果你已经熟悉 SQL 了,就可以跳过这部分内容。

按照惯例, SOL 关键字全部使用大写字母。当然, 也可以不这样做。

SELECT 语句相当灵活。仅使用下面这个查询语句,就可以查出 Books 表中的所有记录:

SELECT \* FROM Books

在每一个 SQL 的 SELECT 语句中,FROM 子句都是必不可少的。FROM 子句用于告知数据库应该在哪个表上查询数据。

我们还可以选择所需要的列:

SELECT ISBN, Price, Title FROM Books

并且还可以在查询语句中使用 WHERE 子句来限定所要选择的行:

SELECT ISBN, Price, Title FROM Books WHERE Price <= 29.95

请小心使用"相等"这个比较操作。与 Java 编程语言不同, SQL 使用 = 和 > 而非 == 和!=来进行相等性比较。

直 注释:有些数据库供应商的产品支持在进行不等于比较时使用!=。这不符合标准 SQL 的语法,所以我们建议不要使用这种方法。

WHERE 子句也可以使用 LIKE 操作符来实现模式匹配。不过,这里的通配符并不是通常使用的\*和?,而是用%表示0或多个字符,用下划线表示单个字符。例如,

SELECT ISBN, Price, Title FROM Books WHERE Title NOT LIKE '%n\_x%'

这条语句排除了所有书名中包含 UNIX 或者 Linux 的图书。

请注意,字符串都是用单引号括起来的,而非双引号。字符串中的单引号则需要用一对 单引号代替。例如,

SELECT Title FROM Books WHERE Title LIKE '%''%'

上述语句会返回所有包含单引号的书名。

你也可以从多个表中选取数据:

SELECT \* FROM Books, Publishers

如果没有 WHERE 子句,上述查询语句就意义不大了,它只是罗列了两个表中所有记录的组合。在我们这个例子中,Books 表有 20 行记录,Publishers 表有 8 行记录,合并的结果将产生 20×8 条记录,其中不乏大量重复数据。实际上我们需要对查询结果进行限制,只对那些图书与出版社相匹配的数据感兴趣。

```
SELECT * FROM Books, Publishers
WHERE Books.Publisher Id = Publishers.Publisher Id
```

这条语句的查询结果共有20行记录,每一条记录对应于一本书,因为每本书都在Publishers表中只对应一个出版社。

每当查询语句涉及多个表时,相同的列名可能会出现在两个不同的地方。在我们的例子中也存在这种情况,Books 表和 Publishers 表都拥有一个列名为 Publisher Id 的列。当出现歧义时,可以在每个列名前添加它所在表的表名作为前缀,比如 Book. Publisher Id。

也可以使用 SQL 来改变数据库中的数据。例如,假设现在要将所有书名中包含"C++"的图书降价 5 美元,可以执行以下语句:

```
UPDATE Books
SET Price = Price - 5.00
WHERE Title LIKE '%C++%'
```

类似地,要删除所有的 C++ 图书,可以使用下面的 DELETE 查询:

```
DELETE FROM Books
WHERE Title LIKE '%C++%'
```

此外,SQL中还有许多内置函数,用于对某一列计算平均值、查找最大值和最小值以及 其他许多功能。在此我们就不讨论了。

典型情况下,可以使用 INSERT 语句向表中插入值:

```
INSERT INTO Books
```

VALUES ('A Guide to the SQL Standard', '0-201-96426-0', '0201', 47.95)

我们必须为每一条插入到表中的记录使用一次 INSERT 语句。

当然,在查询、修改和插入数据之前,必须要有存储数据的位置。可以使用 CREATE TABLE 语句创建一个新表,还可以为每一列指定列名和数据类型。

```
CREATE TABLE Books
(
Title CHAR(60),
ISBN CHAR(13),
Publisher_Id CHAR(6),
Price DECIMAL(10,2)
```

表 5-5 给出了最常见的 SOL 数据类型。

| -        |     | 001 | Mary Li | III 246.5 | CC 1  |
|----------|-----|-----|---------|-----------|-------|
| makers & | 5-5 | SQL | 229U JR | 中フトラ      | reu - |
| ADC. 1   | J-J | OWL | TEX 1/  |           | -64   |
|          |     |     |         |           |       |

| 数据类型          | 说明          |
|---------------|-------------|
| INTEGER 或 INT | 通常为32位的整数   |
| SMALLINT      | 通常为 16 位的整数 |

| 数据<br>型                                 | 明                            |
|-----------------------------------------|------------------------------|
| NUMERIC(n(n)f DECIMAL(n(n)或<br>DEC(m,n) | 其中小数点后为n位<br>m位<br>定点十<br>制数 |
| FLOAT(n)                                | 运算精度为n位二<br>制数<br>浮点数        |
| REAL                                    | 常为32位浮点数                     |
| DOUBLE                                  | 常为64位浮点数                     |
| CHARACTER(n)或 CHAR(n)                   | 固定<br>度为《<br>字               |
| VARCHAR(n)                              | 最大<br>度为<br>可变<br>字<br>串     |
| BOOLEAN                                 | 布尔值                          |
| DATE                                    | 日历日期<br>与具体<br>实<br>关        |
| TIME                                    | 当前时<br>与具体<br>实<br>关         |
| TIMESTAMP                               | 当前日期和时<br>与具体<br>实<br>关      |
| BLOB                                    | 二<br>制大对                     |
| CLOB                                    | 字<br>大对                      |

*在本书中 我们不再介 更多 子句 比如可以应 于CREATE TABLE 句 主 子句和 束子句。*

# *5.3 JDBC 配置*

*当然 你 有一个可 得其JDBC 动 序 数据库 序。 前 方 有 多出 序可供 <sup>择</sup> 比如 IBMDB2、Microsoft SQL Server. MySQL、Oracle <sup>和</sup> PostgreSQL。*

*为了 习本 分内容 你 创建一个数据库 我们假定你将 个数据库命名为 C0REJAVA。你 己创建 或 数据库 员创建 个数据库 并 你拥有 当权 因 为你 拥有对 个数据库 创建、更新和删 权 。*

*如果你以前从未安 客户 /服务器模式 数据库 么就会发 样一个 数据库会 显复杂并且 于 断故 原因。如果安 数据库无法正常 么最好 专 家来帮忙。*

*如果 一次接 数据库 我们建 使 Apache Derby,它可以从http://db.apache.org/ derby处下 到 在某些JDK 本中也包含了它。*

*在 写 一个数据库 序之前 你 收 大 信息和文件 下 将 些内容。*

#### *5.3.1数据库URL*

*在 接数据库时 我们必 使 各 与数据库 型 关 参数 例如主机名、 口号和 数据库名。*

*JDBC使 了一 与普 URL 似 法来描 数据源。下 是 法 两个实例*

*jdbc:derby://localhost:1527/COREJAVA;create=true* 

*jdbc:postgresql:COREJAVA*

*上 JDBC URL指定了名为COREJAVA 一个Derby数据库和一个PostgreSQL数据库。 JDBC URL 一 法为*

*j dbc \subprotocol: other stuff*

*其中 subprotocol 于 择 接到数据库 具体 动 序。*

*other stuff参数 格式 所使用的subprotocol不同 不同。如果 了 具体格式 你 查 数据库供应商提供 关文档。*

#### *5.3.2 动 序JAR文件*

*你 得包含了你所使 数据库 动 序 JAR文件。如果你使用的是Derby, 么就需要derbyclient, jar 如果你使 是其他 数据库 么就 去寻找恰当 <sup>动</sup> 序。例如 PostgreSQL 动 序可以在http://jdbc.postgresql.org处找到。*

*在 数据库 序时 需要将 动 序 JAR文件包括到 径中 编译时并不 个JAR文件 。*

*在从命令 启动 序时 只 使 下 命令*

*java -classpath driverPath:. ProgramName*

*在Windows上 可以使 分号将当前 径 即 .字 径 与 动 序JAR<sup>文</sup> 件分 开。*

#### *5.3.3启动数据库*

*数据库服务器在 接之前 先启动 启动的细节取决于所使用的数据库。*

*在使 Derby数据库时 循下 步*

- *<sup>1</sup>. 打开命令shell,并 到将来存放数据库文件 录中。*
- *<sup>2</sup>. 定位derbyrun.jar。对于某些JDK <sup>本</sup> 它包含在jdk/db/lib 0录中 如果没有包 含 就安 Apache Derby,并定位安 录 JAR文件。我们 derby来表示包含lib/ derbyrun. jar 录<sup>o</sup>*
  - *3. 下 命令*

*java -jar derby/lib/de rby run. <sup>j</sup> <sup>a</sup> <sup>r</sup> server start*

- *4. 仔 检査数据库是否正 工作了。然后创建一个名为ij.properties并包含下 各 文件*
  - *ij•driver=org.apache•derby.jdbc.ClientDriver*
  - *ij ・ protoco> jdbc: derby: //localhost: <sup>1527</sup>/*
  - *ij,database=COREJAVA;create=true*

*在另一^令shell<sup>中</sup> <sup>执</sup> <sup>下</sup> 命令来 Derby 交互式 木执 工具 <sup>为</sup>ij java -jar derby/lib/derbyrun.jar ij -p ij.properties*

*在 可以发布像下 样 SQL命令了*

CREATE TABLE Greetings (Message CHAR(20)); INSERT INTO Greetings VALUES ('Hello, World!'); SELECT \* FROM Greetings; DROP TABLE Greetings;

注意,每条命令都需要以分号结尾。要退出编辑器,可以键入 EXIT:

5. 在使用完数据库之后,可以用下面的命令关闭服务器:

java -jar derby/lib/derbyrun.jar server shutdown

如果使用其他的数据库,则需要查看文档,以了解如何启动和关闭数据库服务器,以及如何连接到数据库和发布 SQL 命令。

#### 5.3.4 注册驱动器类

许多 JDBC 的 JAR 文件 (例如 ApacheDerby 驱动程序) 会自动注册驱动器类,在这种情况下,可以跳过本节所描述的手动注册步骤。包含 META-INF/services/java.sql.Driver 文件的 JAR 文件可以自动注册驱动器类,解压缩驱动程序 JAR 文件就可以检查其是否包含该文件。

如果驱动程序 JAR 文件不支持自动注册,那就需要找出数据库提供商使用的 JDBC 驱动器类的名字。典型的驱动器名字如下:

org.apache.derby.jdbc.ClientDriver org.postgresql.Driver

通过使用 DriverManager,可以用两种方式来注册驱动器。一种方式是在 Java 程序中加载驱动器类、例如:

Class.forName("org.postgresql.Driver"); // force loading of driver class

这条语句将使得驱动器类被加载,由此将执行可以注册驱动器的静态初始化器。

另一种方式是设置 jdbc.drivers 属性。可以用命令行参数来指定这个属性,例如:

 ${\tt java-Djdbc.drivers=org.postgresql.Driver}\ Program Name$ 

或者在应用中用下面这样的调用来设置系统属性

System.setProperty("jdbc.drivers", "org.postgresql.Driver");

在这种方式中可以提供多个驱动器,用冒号将它们分隔开,例如

org.postgresql.Driver:org.apache.derby.jdbc.ClientDriver

#### 5.3.5 连接到数据库

在 Java 程序中, 我们可以用下面这样的代码打开一个数据库连接:

String url = "jdbc:postgresql:COREJAVA";
String username = "dbuser";
String password = "secret";
Connection conn = DriverManager.getConnection(url, username, password);

驱动管理器会遍历所有注册过的驱动程序,以便找到一个能够使用数据库 URL 中指定的子协议的驱动程序。

getConnection 方法返回一个 Connection 对象。在下一节中,我们将详细介绍如何使用 Connection 对象来执行 SOL 语句。

要连接到数据库, 我们还需要知道数据库的名字和密码。

直 注释:在默认情况下,Derby允许我们使用任何用户名进行连接,并且不检查密码。它会为每个用户生成一个单独的表集合,而默认的用户名是 app。

程序清单 5-1 中的测试程序将所有这些步骤放到了一起:它从名为 database.properties 的文件中加载连接参数,并连接到数据库。示例代码中提供的 database.properties 文件包含的是关于 Derby 数据库的连接信息,如果使用其他的数据库,则需要将与数据库相关的连接信息放到这个文件中。下面是一个用于连接到 PostgreSQL 数据库的示例:

jdbc.drivers=org.postgresql.Driver jdbc.url=jdbc:postgresql:COREJAVA jdbc.username=dbuser jdbc.password=secret

在连接到数据库之后,这个测试程序执行了下面的 SQL 语句:

CREATE TABLE Greetings (Message CHAR(20))
INSERT INTO Greetings VALUES ('Hello, World!')
SELECT \* FROM Greetings

SELECT 语句的结果将被打印出来,你应该可以看到如下的输出:

Hello, World!

然后,通过执行下面的语句移除这张表:

DROP TABLE Greetings

要运行这个测试程序,需要按照前面所描述的方式启动数据库,并像下面这样启动这个程序:

java -classpath .: driverJAR test.TestDB

(Windows 用户需要注意,用;代替:来分隔路径元素。)

☑ 提示:调试与JDBC相关的问题时,有种方法是启用JDBC的跟踪机制。调用Driver-Manager.setLogWriter方法可以将跟踪信息发送给PrintWriter,而PrintWriter将输出JDBC活动的详细列表。大多数JDBC驱动程序的实现都提供了用于跟踪的附加机制,例如,在使用Derby时,可以在JDBC的URL中添加traceFile选项,如jdbc:derby://localhost:1527/COREJAVA;create=true;traceFile=trace.out。

#### 程序清单 5-1 test/TestDB.java

<sup>1</sup> package test;

```
3 import java.nio.file.*;
4 import java.sql.*;
5 import java.io.*;
6 import java.nio.charset.*;
7 import java.util.*;
9 /**
    * This program tests that the database and the JDBC driver are correctly configured.
10
    * @version 1.04 2021-06-17
    * @author Cay Horstmann
13
14 public class TestDB
15 {
      public static void main(String args[]) throws IOException
16
17
         try
18
19
            runTest();
21
         catch (SQLException e)
22
23
         {
            for (Throwable t : e)
24
               t.printStackTrace();
25
      1
27
28
29
       * Runs a test by creating a table, adding a value, showing the table contents, and
30
       * removing the table.
31
32
      public static void runTest() throws SQLException, IOException
33
34
         try (Connection conn = getConnection();
35
                Statement stat = conn.createStatement())
36
37
             stat.executeUpdate("CREATE TABLE Greetings (Message CHAR(20))");
38
             stat.executeUpdate("INSERT INTO Greetings VALUES ('Hello, World!')");
39
48
             try (ResultSet result = stat.executeQuery("SELECT * FROM Greetings"))
42
                if (result.next())
43
                   System.out.println(result.getString(1));
45
             stat.executeUpdate("DROP TABLE Greetings");
46
47
          }
      }
48
49
        * Gets a connection from the properties specified in the file database.properties.
51
        * @return the database connection
52
53
       public static Connection getConnection() throws SQLException, IOException
54
55
          var props = new Properties();
56
57
          try (Reader in = Files.newBufferedReader(
```

```
Path.of("database.properties"), StandardCharsets.UTF 8))
58
59
68
            props.load(in);
61
         String drivers = props.getProperty("idbc.drivers");
62
         if (drivers != null) System.setProperty("jdbc.drivers", drivers);
63
         String url = props.getProperty("jdbc.url");
64
         String username = props.getProperty("idbc.username"):
65
         String password = props.getProperty("jdbc.password");
66
67
         return DriverManager.getConnection(url, username, password);
68
69
78 }
```

#### API java.sql.DriverManager

static Connection getConnection(String url, String user, String password)
 建立一个到指定数据库的连接,并返回一个 Connection 对象。

#### 5.4 使用 JDBC 语句

在下面各节中,你将会看到如何使用 JDBC Statement 来执行 SQL 语句,获得执行结果,以及处理错误。然后,我们将向你展示一个操作数据库的简单示例。

#### 5.4.1 执行 SQL 语句

在执行 SQL 语句之前,首先需要创建一个 Statement 对象。要创建 Statement 对象,需要使用调用 DriverManager.getConnection 方法所获得的 Connection 对象。

Statement stat = conn.createStatement();

接着,把要执行的 SQL 语句放入字符串中,例如:

```
String command = "UPDATE Books"
    + " SET Price = Price - 5.00"
    + " WHERE Title NOT LIKE '%Introduction%'";
```

然后,调用 Statement 接口中的 executeUpdate 方法:

```
stat.executeUpdate(command);
```

executeUpdate 方法将返回受 SQL 语句影响的行数,或者对不返回行数的语句返回 0。例如,在先前的例子中调用 executeUpdate 方法将返回那些降价 5 美元的行数。

executeUpdate 方法既可以执行诸如 INSERT、UPDATE 和 DELETE 之类的操作,也可以执行诸如 CREATE TABLE 和 DROP TABLE 之类的数据定义语句。但是,执行 SELECT 查询时必须使用 executeQuery 方法。另外还有一个 execute 语句可以执行任意的 SQL 语句,此方法通常只用于由用户提供的交互式查询。

当我们执行查询操作时,通常感兴趣的是查询结果。executeQuery方法会返回一个 ResultSet 类型的对象,可以通过它来每次一行地迭代遍历所有查询结果。

```
ResultSet rs = stat.executeQuery("SELECT * FROM Books");
分析结果集时通常可以使用类似如下的基础循环:
while (rs.next())
{
    look at a row of the result set
}
```

● 警告: ResultSet 接口的迭代协议与 java.util.Iterator 接口稍有不同。对于 ResultSet 接口, 迭代器初始化时被设定在第一行之前的位置, 必须调用 next 方法将它移动到第一行。另外, 它没有 hasNext 方法, 我们需要不断地调用 next, 直至该方法返回 false。

结果集中行的顺序是任意排列的。除非使用 ORDER BY 子句指定行的顺序,否则不能为行序强加任何意义。

查看每一行时,可能希望知道其中每一列的内容,有许多访问器(accessor)方法可以用于获取这些信息。

```
String isbn = rs.getString(1);
double price = rs.getDouble("Price");
```

不同的数据类型有不同的访问器,比如 getString 和 getDouble。每个访问器都有两种形式,一种接受数字型参数,另一种接受字符串参数。当使用数字型参数时,我们指的是该数字所对应的列。例如,rs.getString(1) 返回的是当前行中第一列的值。

● 警告:与数组的索引不同,数据库的列序号是从1开始计算的。

当使用字符串参数时,指的是结果集中以该字符串为列名的列。例如,rs.getDouble ("Price") 返回列名为 Price 的列所对应的值。使用数字型参数效率更高一些,但是使用字符串参数可以使代码易于阅读和维护。

当 get 方法的类型和列的数据类型不一致时,每个 get 方法都会进行合理的类型转换。例如,调用 rs.getString("Price") 时,该方法会将 Price 列的浮点值转换成字符串。

#### appl java.sql.Connection

- Statement createStatement()
   创建一个 Statement 对象,用以执行不带参数的 SQL 查询和更新。
- void close()
   立即关闭当前的连接,并释放由它所创建的 JDBC 资源。

#### API java.sql.Statement

- ResultSet executeQuery(String sqlQuery)
   执行给定字符串中的 SQL 语句,并返回一个用于查看查询结果的 ResultSet 对象。
- int executeUpdate(String sqlStatement)
- long executeLargeUpdate(String sqlStatement)

执行字符串中指定的 INSERT、UPDATE 或 DELETE 等 SQL 语句。还可以执行数据定义语言(Data Definition Language, DDL)的语句,如 CREATE TABLE。返回受影响的行数,如果是没有更新计数的语句,则返回 0。

• boolean execute(String sqlStatement)

执行字符串中指定的 SQL 语句。可能会产生多个结果集和更新计数。如果第一个执行结果是结果集,则返回 true; 反之, 返回 false。调用 getResultSet 或 getUpdateCount 方法可以得到第一个执行结果。请参见 5.5.4 节中关于处理多结果集的详细信息。

ResultSet getResultSet()

返回前一条查询语句的结果集。如果前一条语句未产生结果集,则返回 null 值。对于每一条执行过的语句,该方法只能被调用一次。

- int getUpdateCount()
- long getLargeUpdateCount() 8

返回受前一条更新语句影响的行数。如果前一条语句未更新数据库,则返回-1。对于每一条执行过的语句,该方法只能被调用一次。

- void close() 关闭该语句对象以及它所对应的结果集。
- boolean isClosed() 6
   如果该语句被关闭,则返回 true。
- void closeOnCompletion() 7
  - 一旦该语句的所有结果集都被关闭,则关闭该语句。

#### API java.sql.ResultSet

boolean next()

将结果集中的当前行向前移动一行。如果已经到达最后一行的后面,则返回 false。 注意,初始情况下必须调用该方法才能转到第一行。

- Xxx getXxx(int columnNumber)
- Xxx getXxx(String columnLabel)
   (Xxx 指数据类型,例如 int、double、String 和 Date 等。)
- <T> T getObject(int columnIndex, Class<T> type) 7
- <T> T getObject(String columnLabel, Class<T> type) 7
- void updateObject(int columnIndex, Object x, SQLType targetSqlType)
- void updateObject(String columnLabel, Object x, SQLType targetSqlType) 8
   用给定的列序号或列标签返回或更新该列的值,并将值转换成指定的类型。列标签是SQL的 AS 子句中指定的标签,在没有使用 AS 时,列标签就是列名。
- int findColumn(String columnName)
   根据给定的列名,返回该列的序号。

- void close()立即关闭当前的结果集。
- boolean isClosed() 6
   如果该语句被关闭,则返回 true。

#### 5.4.2 管理连接、语句和结果集

每个 Connection 对象都可以创建一个或多个 Statement 对象。同一个 Statement 对象可以用于多个不相关的命令和查询。但是,一个 Statement 对象最多只能有一个打开的结果集。如果需要执行多个查询操作,且需要同时分析查询结果,那么必须创建多个 Statement 对象。

需要说明的是,每个链接上的语句数是有限制的。使用 DatabaseMetaData 接口中的 getMaxStatements 方法可以获取 JDBC 驱动程序支持的同时打开的语句对象的总数。

实际上,我们通常并不需要同时处理多个结果集。如果结果集相互关联,我们可以使用组合查询,这样就只需要分析一个结果。对数据库进行组合查询比使用 Java 程序遍历多个结果集要高效得多。

我们应该确保在一个 Statement 对象上触发新的查询或更新语句之前结束对所有结果集的处理,因为前序查询的所有结果集都会被自动关闭。

使用完 ResultSet、Statement 或 Connection 对象后,应立即调用 close 方法。这些对象都使用了规模较大的数据结构,它们会占用数据库存服务器上的有限资源。

Statement 对象的 close 方法将自动关闭所有与其相关联的结果集。同样地,调用 Connection 类的 close 方法将关闭该连接上的所有语句。

反过来的情况是,可以在 Statement 上调用 closeOnCompletion 方法,在其所有结果集都被关闭后,该语句会立即被自动关闭。

如果所用连接都是短时的,那么无须操心语句和结果集的关闭。只需将 close 语句放在带资源的 try 语句中,以便确保连接对象不可能继续保持打开状态。

```
try (Connection conn = . . .)
{
   Statement stat = conn.createStatement();
   ResultSet result = stat.executeQuery(queryString);
   process query result
}
```

#### 5.4.3 分析 SQL 异常

每个 SQLException 都有一个由多个 SQLException 对象构成的链,这些对象可以通过 getNext-Exception 方法获取。这个异常链是每个异常都具有的由 Throwable 对象构成的"成因"链之外的异常链(请参见卷 I 第7章以了解 Java 异常的详细信息),因此,我们需要用两个嵌套的循环来完整枚举所有的异常。幸运的是, SQLException 类得到了增强,实现了Iterable<Throwable>接口,其iterator()方法可以产生一个 Iterator<Throwable>,这个迭代器可以迭代这两个链,首先迭代第一个 SQLException 的成因链,然后迭代下一个

*SQLException,以此 推。我们可以 接使 下 个改 for循*

```
for Throwable t : sqlException
{
  do something with t
}
```

*可以在SQLException上 getSQLState和getErrorCode方法来 一步分析它 其中 一个 方法将产生符合x/open或SQL 2003标准 字 串 DatabaseMetaData接口 getSQLState-Type方法可以査出 动 序所使 标准 。 代 是与具体 提供商 关 。*

*SQL异常按照层次 构树 方式 到了一 如图5。5所 使得我们可以按照与 提供商无关 方式来捕 具体 型。*

![](_page_38_Figure_6.jpeg)

*另外 数据库 动 序可以将 命 作为 告报告 我们可以从 接、 句和 果 中 取 些 告。SQLWarning 是SQLException 子 尽 SQLWarning不会 当作异常 抛出 我们可以 getSQLState和getErrorCode来 取有关 告 更多信息。与SQL异常 似 告也是串成 。 得所有 告 可以使 下 循*

```
SQLWarning w = stat.getWarningO; 
while (w != null)
```

```
246
```

```
do something with w
w = w.nextWarning();
}
```

当数据从数据库中读出并意外被截断时, SQLWarning 的 DataTruncation 子类就派上用场了。如果数据截断发生在更新语句中, 那么 DataTruncation 对象将会被当作异常抛出。

#### API java.sql.SQLException

- SQLException getNextException()
   返回链接到该 SQL 异常的下一个 SQL 异常,或者在到达链尾时返回 null。
- Iterator<Throwable> iterator() 6 获取迭代器,可以迭代链接的 SQL 异常和它们的成因。
- String getSQLState() 获取 "SQL 状态",即标准化的错误代码。
- int getErrorCode()获取提供商相关的错误代码。

#### API java.sql.SQLWarning

SQLWarning getNextWarning()
 返回链接到该警告的下一个警告,或者在到达链尾时返回 null。

# java.sql.Connection 1.1 java.sql.Statement 1.1 java.sql.ResultSet 1.1

SQLWarning getWarnings()
 返回未处理警告中的第一个,或者在没有未处理警告时返回 null。

#### API java.sql.DataTruncation

- boolean getParameter()
   如果在参数上进行了数据截断,则返回 true;如果在列上进行了数据截断,则返回 false。
- int getIndex()返回被截断的参数或列的索引。
- int getDataSize()
   返回应该已经被传输的字节数量,或者在该值未知的情况下返回-1。
- int getTransferSize()
   返回实际已经被传输的字节数量,或者在该值未知的情况下返回-1。

#### 5.4.4 组装数据库

至此,大家也许都迫不及待地想编写一个真正实用的 JDBC 程序了。如果我们可以编写

一段程序来执行之前所介绍的那些巧妙的查询,那当然很好。不过,在此之前我们还有一个问题没有解决:目前数据库中还没有数据。我们需要组装数据库,并且也确实存在一种简单方法可以实现此目的:用一系列的 SQL 指令来创建数据表并向其中插入数据。大多数数据库程序都可以处理来自文本文件中的一系列 SQL 指令,但是在语句终止符和其他一些文法问题上,这些数据库程序之间存在着令人讨厌的差异。

正是由于这个原因,我们使用 JDBC 创建了一个简单的程序,它从文件中读取 SQL 指令,其中一条指令占据一行,然后执行它们。

该程序专门用于从下列格式的文本文件中读取数据:

```
CREATE TABLE Publishers (Publisher_Id CHAR(6), Name CHAR(30), URL CHAR(80)); INSERT INTO Publishers VALUES ('0201', 'Addison-Wesley', 'www.aw-bc.com'); INSERT INTO Publishers VALUES ('0471', 'John Wiley & Sons', 'www.wiley.com');
```

程序清单 5-2 是用来读取 SQL 语句文件以及执行这些语句的程序代码。你没必要去通读这些代码,我们在这里只是提供了这样的程序,使你能够组装数据库并运行本章剩余部分的代码。

请确认你的数据库服务器是在运行的,然后可以使用如下方法运行该程序:

```
java -classpath driverPath:. exec.ExecSQL Books.sql
java -classpath driverPath:. exec.ExecSQL Authors.sql
java -classpath driverPath:. exec.ExecSQL Publishers.sql
java -classpath driverPath:. exec.ExecSQL BooksAuthors.sql
```

在运行程序之前,请检查一下 database.properties 文件是否已经针对你的运行环境进行了正确设置。请查看 5.3.5 节。

直 注释:你的数据库可能也包含直接读取 SQL 文件的工具,例如,在使用 Derby 时,可以运行下面的命令:

java -jar derby/lib/derbyrun.jar ij -p ij.properties Books.sql

(ij.properties 文件在 5.3.3 节中描述过。)

在用于 ExecSQL 命令的数据格式中, 我们允许每行的结尾都可以有一个可选的分号, 因为大多数数据库工具都希望使用这种格式。

下面将简要介绍一下 ExecSQL 程序的操作步骤。

- 1. 连接数据库。getConnection 方法读取 database.properties 文件中的属性信息,并将属性 jdbc.drivers 添加到系统属性中。驱动程序管理器使用属性 jdbc.drivers 加载相应的驱动程序。getConnection 方法使用 jdbc.url、jdbc.username 和 jdbc.password 等属性打开数据库连接。
  - 2. 打开包含 SQL 语句的文件。如果未提供任何文件名,则在控制台中提示用户输入语句。
- 3. 使用泛化的 execute 方法执行每条语句。如果它返回 true,则说明该语句产生了一个结果集。我们为图书数据库提供的 4 个 SQL 文件都以一条 SELECT \* 语句结束,这样就可以看到数据是否已成功插入到了数据库中。
  - 4. 如果产生了结果集,则打印出结果。因为这是一个泛化的结果集,所以我们必须使用

元数据来确定该结果的列数。更多的信息请查看 5.8 节。

- 5. 如果运行过程中出现 SQL 异常,则打印出这个异常以及所有可能包含在其中的与其链接在一起的相关异常。
  - 6. 关闭数据库连接。

程序清单 5-2 给出了该程序的代码。

#### 程序清单 5-2 exec/ExecSQL.java

```
1 package exec;
2
3 import java.io.*;
4 import java.nio.charset.*;
5 import java.nio.file.*;
6 import java.util.*;
7 import java.sql.*;
8
9 /**
   * Executes all SQL statements in a file. Call this program as <br/>
   * java -classpath driverPath:. ExecSQL commandFile
12
    * @version 1.34 2021-06-17
13
   * @author Cav Horstmann
14
16 class ExecSQL
17
   {
      public static void main(String args[]) throws IOException
19
         try (Scanner in = args.length == 0 ? new Scanner(System.in)
20
               : new Scanner(Path.of(args[0]), StandardCharsets.UTF 8))
22
            try (Connection conn = getConnection();
23
                   Statement stat = conn.createStatement())
25
               while (true)
26
                   if (args.length == 0) System.out.println("Enter command or EXIT to exit:");
28
29
                   if (!in.hasNextLine()) return;
31
                   String line = in.nextLine().strip();
32
                   if (line.equalsIgnoreCase("EXIT")) return;
33
                   if (line.endsWith(";")) // remove trailing semicolon
34
                      line = line.substring(0, line.length() - 1);
35
                   try
36
37
                      boolean isResult = stat.execute(line);
38
                      if (isResult)
39
40
                         try (ResultSet rs = stat.getResultSet())
41
42
                            showResultSet(rs);
43
44
                      }
45
```

```
else
46
47
                         int updateCount = stat.getUpdateCount();
48
                         System.out.println(updateCount + " rows updated");
49
58
51
                   catch (SQLException e)
53
                      for (Throwable t : e)
54
                         t.printStackTrace();
55
56
57
58
59
68
         catch (SQLException e)
61
         {
            for (Throwable t : e)
67
                t.printStackTrace();
63
64
      }
65
66
67
       * Gets a connection from the properties specified in the file database.properties
68
       * @return the database connection
69
78
      public static Connection getConnection() throws SQLException, IOException
71
72
         var props = new Properties();
73
         try (Reader in = Files.newBufferedReader(
74
               Path.of("database.properties"), StandardCharsets.UTF 8))
75
76
            props.load(in);
77
78
         String drivers = props.getProperty("jdbc.drivers");
79
         if (drivers != null) System.setProperty("jdbc.drivers", drivers);
88
81
         String url = props.getProperty("jdbc.url");
82
         String username = props.getProperty("jdbc.username");
83
         String password = props.getProperty("jdbc.password");
85
         return DriverManager.getConnection(url, username, password);
86
      }
87
88
89
       * Prints a result set.
98
       * @param result the result set to be printed
91
92
      public static void showResultSet(ResultSet result) throws SQLException
93
94
95
         ResultSetMetaData metaData = result.getMetaData();
         int columnCount = metaData.getColumnCount();
96
97
         for (int i = 1; i <= columnCount; i++)
99
            if (i > 1) System.out.print(", ");
100
```

```
System.out.print(metaData.getColumnLabel(i));
181
182
          System.out.println();
103
184
         while (result.next())
105
186
             for (int i = 1; i <= columnCount; i++)
187
188
                if (i > 1) System.out.print(", ");
189
                System.out.print(result.getString(i));
110
             System.out.println();
112
113
      }
114
115 }
```

#### 5.5 执行查询操作

在这一节中,我们将编写一段用于对 COREJAVA 数据库执行查询操作的程序。为了使程序可以正常运行,必须按照上一节中的说明用表组装 COREJAVA 数据库。

在查询数据库时,可以选择作者和出版社,或者将这两项中的一项设置为"Any"。

还可以修改数据库中的数据。选择一家出版社,然后输入金额。该出版社对应的所有价格都将按照填入的金额进行调整,同时程序将显示被修改的行数。修改完价格以后,可以运行一个查询操作,以核实新的价格。

#### 5.5.1 预备语句

在这个程序中,我们使用了一个新的特性,即预备语句(prepared statement)。如果我们要查询某个出版社的所有图书而不考虑具体的作者,那么该查询的 SQL 语句如下:

```
SELECT Books.Price, Books.Title
FROM Books, Publishers
WHERE Books.Publisher_Id = Publishers.Publisher_Id
AND Publishers.Name = the name from the list box
```

我们没有必要在每次触发一个这样的查询时都建立新的查询语句,而是可以准备一个带有宿主变量的查询语句,每次查询时只需为该变量填入不同的字符串就可以反复多次地使用该语句。这一技术改进了查询性能,每当数据库执行一个查询时,它总是首先通过计算来确定查询策略,以便高效地执行查询操作。通过事先准备好查询并多次重用它,我们就可以确保查询所需的准备步骤只执行一次。

在预备查询语句中,每个宿主变量都用"?"来表示。如果存在一个以上的变量,那么在设置变量值时必须注意"?"的位置。例如,如果我们的预备查询为如下形式:

```
String publisherQuery
```

+ " WHERE Books.Publisher\_Id = Publishers.Publisher\_Id AND Publishers.Name = ?";
PreparedStatement stat = conn.prepareStatement(publisherQuery);

在执行预备语句之前,必须使用 set 方法将变量绑定到实际的值上。和 ResultSet 接口中的 get 方法类似,针对不同的数据类型也有不同的 set 方法。在本例中,我们为出版社名称设置了一个字符串值。

stat.setString(1, publisher);

第一个参数指的是需要设置的宿主变量的位置,位置1表示第一个"?"。第二个参数指的是赋予宿主变量的值。

如果想要重用已经执行过的预备查询语句,那么除非使用 set 方法或调用 clearParameters 方法,否则所有宿主变量的绑定都不会改变。这就意味着,在从一个查询到另一个查询的过程中,只需使用 setXxx 方法重新绑定那些需要改变的变量即可。

一旦为所有变量都绑定了具体的值,就可以执行预备语句了:

ResultSet rs = stat.executeQuery();

√ 提示: 通过连接字符串来手动构建查询显得非常枯燥乏味,而且存在潜在的危险。你必须注意像引号这样的特殊字符,而且如果查询中涉及用户的输入,那就还需要警惕注入攻击。因此,只要查询涉及变量,就应该使用预备语句。

价格更新操作可以由 UPDATE 语句实现。请注意,我们调用的是 executeUpdate 方法,而非 executeQuery 方法,因为 UPDATE 语句不返回结果集。executeUpdate 的返回值是被修改过的行数。

int r = stat.executeUpdate();
System.out.println(r + " rows updated");

i 注释: 在相关的 Connection 对象关闭之后, PreparedStatement 对象也就变得无效了。不过, 许多数据库通常都会自动缓存预备语句。如果相同的查询被预备两次, 数据库通常会直接重用查询策略。因此, 无须过多考虑调用 prepareStatement 的开销。

下面简要说明示例程序的结构:

- 通过执行两个查询得到数据库中所有的作者和出版社名称,作者和出版社数组列表由此组装而成。
- 涉及作者的查询比较复杂。因为一本书可能有多个作者, BooksAuthors 表给出了作者和图书之间的对应关系。例如, ISBN 号为 0-201-96426-0 的图书有两个作者, 其代号为: DATE 和 DARW。以下为 BooksAuthors 表中的两行记录:

0-201-96426-0, DATE, 1 0-201-96426-0, DARW, 2

BooksAuthors 表中第三列指的是作者的顺序(我们不能用表中行的位置来表示作者顺序,因为在关系表中没有固定的行顺序)。因此,查询时需要连接 Books 表、BooksAuthors 表和 Authors 表,以便和用户所选的作者名进行比较。

SELECT Books.Price, Books.Title FROM Books, BooksAuthors, Authors, Publishers
WHERE Authors.Author\_Id = BooksAuthors.Author\_Id AND BooksAuthors.ISBN = Books.ISBN
AND Books.Publisher\_Id = Publishers.Publisher\_Id AND Authors.Name = ?
AND Publishers.Name = ?

- ☑ 提示:许多程序员都不喜欢使用如此复杂的 SQL 语句。比较常见的方法是使用大量的 Java 代码来迭代多个结果集,但是这种方法效率非常低。通常,使用数据库的查询代码要比使用 Java 程序好得多——这是数据库的核心竞争力之一。一般而言,可以使用 SQL 解决的问题,就不要使用 Java 程序。
  - change Prices 方法执行了一条 UPDATE 语句。注意, UPDATE 语句中的 WHERE 子句需要使用出版社代码,而我们只知道出版社名称。这个问题可以使用嵌套子查询来解决。

```
UPDATE Books
SET Price = Price + ?
WHERE Books.Publisher_Id = (SELECT Publisher_Id FROM Publishers WHERE Name = ?)
```

程序清单 5-3 给出了程序的完整代码。

#### 程序清单 5-3 query/QueryTest.java

```
1 package query;
3 import java.io.*;
4 import java.nio.charset.*;
5 import java.nio.file.*;
6 import java.sql.*;
7 import java.util.*;
9 /**
* This program demonstrates several complex database queries.
11 * @version 1.32 2021-06-17
12 * @author Cay Horstmann
13 */
14 public class QueryTest
15 {
      private static final String allQuery = "SELECT Books.Price, Books.Title FROM Books";
17
      private static final String authorPublisherQuery = """
19 SELECT Books.Price, Books.Title
20 FROM Books, BooksAuthors, Authors, Publishers
21 WHERE Authors. Author Id = BooksAuthors. Author Id
      AND BooksAuthors.ISBN = Books.ISBN
      AND Books.Publisher Id = Publishers.Publisher Id
    AND Authors Name = ?
      AND Publishers.Name = ?
25
26 """;
27
      private static final String authorQuery = """
28
29 SELECT Books. Price, Books. Title FROM Books, BooksAuthors, Authors
30 WHERE Authors. Author Id = BooksAuthors. Author Id"
    AND BooksAuthors.ISBN = Books.ISBN"
31
      AND Authors. Name = ?
33 """;
```

```
34
      private static final String publisherQuery = """
35
  SELECT Books.Price, Books.Title FROM Books, Publishers
36
   WHERE Books.Publisher Id = Publishers.Publisher Id
      AND Publishers.Name = ?
38
   иии:
39
48
      private static final String priceUpdate = """
41
   UPDATE Books SET Price = Price + ? "
42
   WHERE Books. Publisher Id =
      (SELECT Publisher Id FROM Publishers WHERE Name = ?)
44
45
46
      private static Scanner in;
47
      private static ArrayList<String> authors = new ArrayList<>();
48
49
      private static ArrayList<String> publishers = new ArrayList<>();
58
      public static void main(String[] args) throws IOException
51
52
         try (Connection conn = getConnection())
53
54
             in = new Scanner(System.in);
55
             authors.add("Any");
56
             publishers.add("Any");
57
             try (Statement stat = conn.createStatement())
58
59
                // Fill the authors array list
68
                String query = "SELECT Name FROM Authors";
51
                try (ResultSet rs = stat.executeQuery(query))
62
                {
                   while (rs.next())
64
65
                       authors.add(rs.getString(1));
66
67
                // Fill the publishers array list
                query = "SELECT Name FROM Publishers";
69
                try (ResultSet rs = stat.executeQuery(query))
78
71
                   while (rs.next())
72
73
                       publishers.add(rs.getString(1));
74
75
             boolean done = false;
76
             while (!done)
77
78
                System.out.print("Q)uery C)hange prices E)xit: ");
79
                String input = in.next().toUpperCase();
88
                if (input.equals("Q"))
81
                   executeQuery(conn);
82
                else if (input.equals("C"))
83
                    changePrices(conn);
84
                else
85
                   done = true:
85
87
88
```

stat.setString(2, publisher);

int r = stat.executeUpdate();

142

254

```
catch (SQLException e)
99
90
         {
91
             for (Throwable t : e)
                System.out.println(t.getMessage());
92
93
      }
94
95
96
       * Executes the selected query.
97
       * @param conn the database connection
98
      private static void executeQuery(Connection conn) throws SQLException
188
101
         String author = select("Authors:", authors);
182
         String publisher = select("Publishers:", publishers);
183
104
         PreparedStatement stat;
         if (!author.equals("Any") && !publisher.equals("Any"))
105
186
             stat = conn.prepareStatement(authorPublisherQuery);
197
188
             stat.setString(1, author);
             stat.setString(2, publisher);
189
118
         else if (!author.equals("Any") && publisher.equals("Any"))
111
         {
112
              stat = conn.prepareStatement(authorQuery);
113
114
              stat.setString(1, author);
         else if (author.equals("Any") && !publisher.equals("Any"))
116
117
              stat = conn.prepareStatement(publisherQuery);
              stat.setString(1, publisher);
119
128
         else
             stat = conn.prepareStatement(allQuery);
122
123
         try (ResultSet rs = stat.executeQuery())
125
             while (rs.next())
                System.out.println(rs.getString(1) + ", " + rs.getString(2));
127
128
      }
129
138
131
       * Executes an update statement to change prices.
132
       * @param conn the database connection
133
134
135
      public static void changePrices(Connection conn) throws SQLException
136
137
          String publisher = select("Publishers:", publishers.subList(1, publishers.size()));
          System.out.print("Change prices by: ");
          double priceChange = in.nextDouble();
130
          PreparedStatement stat = conn.prepareStatement(priceUpdate);
148
141
          stat.setDouble(1, priceChange);
```

```
System.out.println(r + " records updated.");
144
145
146
      /**
147
148
       * Asks the user to select a string.
       * @param prompt the prompt to display
149
       * @param options the options from which the user can choose
150
       * @return the option that the user chose
151
       */
152
      public static String select(String prompt, List<String> options)
153
154
         while (true)
155
156
            System.out.println(prompt);
157
            for (int i = 0; i < options.size(); i++)
158
                System.out.printf("%2d) %s%n", i + 1, options.get(i));
159
            int sel = in.nextInt();
168
            if (sel > 0 && sel <= options.size())
161
                return options.get(sel - 1);
162
164
165
166
       * Gets a connection from the properties specified in the file database.properties.
167
       * @return the database connection
168
       */
169
      public static Connection getConnection() throws SQLException, IOException
178
171
         var props = new Properties();
          try (Reader in = Files.newBufferedReader(
173
                Path.of("database.properties"), StandardCharsets.UTF 8))
174
175
             props.load(in);
176
          }
177
178
          String drivers = props.getProperty("idbc.drivers");
179
          if (drivers != null) System.setProperty("jdbc.drivers", drivers);
188
181
          String url = props.getProperty("jdbc.url");
182
          String username = props.getProperty("jdbc.username");
183
          String password = props.getProperty("jdbc.password");
184
185
          return DriverManager.getConnection(url, username, password);
187
188 }
```

#### API java.sql.Connection

 PreparedStatement prepareStatement(String sql)
 返回一个含预编译语句的 PreparedStatement 对象。字符串 sql 代表一个 SQL 语句, 该语句可以包含一个或多个由?字符指明的参数占位符。

#### API java.sql.PreparedStatement

- void setXxx(int n, Xxx x)
   (Xxx 指 int、double、String、Date 之类的数据类型)设置第 n 个参数值为 x。
- void clearParameters()
   清除预备语句中的所有当前参数。
- ResultSet executeQuery()
   执行预备 SQL 查询,并返回一个 ResultSet 对象。
- int executeUpdate()

执行预备 SQL 语句 INSERT、UPDATE 或 DELETE, 这些语句由 PreparedStatement 对象表示。该方法返回在执行上述语句过程中所有受影响的记录总数。如果执行的是数据定义语言(DDL)中的语句,如 CREATE TABLE,则该方法返回 0。

#### 5.5.2 读写 LOB

除了数字、字符串和日期之外,许多数据库还可以存储大对象,例如图片或其他数据。在 SQL 中,二进制大对象称为 BLOB,字符型大对象称为 CLOB。

要读取 LOB,需要执行 SELECT 语句,然后在 ResultSet 上调用 getBlob 或 getClob 方法,这样就可以获得 Blob 或 Clob 类型的对象。要从 Blob 中获取二进制数据,可以调用 getBytes 或 getBinaryStream。例如,如果你有一张保存图书封面图像的表,那么就可以像下面这样获取一张图像:

```
PreparedStatement stat = conn.prepareStatement("SELECT Cover FROM BookCovers WHERE ISBN=?");
...
stat.set(1, isbn);
try (ResultSet result = stat.executeQuery())
{
   if (result.next())
   {
      Blob coverBlob = result.getBlob(1);
      Image coverImage = ImageIO.read(coverBlob.getBinaryStream());
   }
}
```

类似地,如果获取了 Clob 对象,那么就可以通过调用 getSubString 或 getCharacterStream 方法来获取其中的字符数据。

要将 LOB 置于数据库中,需要在 Connection 对象上调用 createBlob 或 createClob, 然后获取一个用于该 LOB 的输出流或写出器,写出数据,并将该对象存储到数据库中。例如,下面展示了如何存储一张图像:

```
Blob coverBlob = connection.createBlob();\nint offset = 0;
OutputStream out = coverBlob.setBinaryStream(offset);
ImageIO.write(coverImage, "PNG", out);
PreparedStatement stat = conn.prepareStatement("INSERT INTO Cover VALUES (?, ?)");
stat.set(1, isbn);
```

#### API java.sql.ResultSet 1.1

- Blob getBlob(int columnIndex) 1.2
- Blob getBlob(String columnLabel) 1.2
- Clob getClob(int columnIndex) 1.2
- Clob getClob(String columnLabel) 1.2 获取给定列的 BLOB 或 CLOB。

#### API java.sql.Blob 1.2

- long length() 获取该 BLOB 的长度。
- byte[] getBytes(long startPosition, long length)
   获取该 BLOB 中给定范围的数据。
- InputStream getBinaryStream()
- InputStream getBinaryStream(long startPosition, long length)
   返回一个输入流,用于读取该 BLOB 中全部或给定范围的数据。
- OutputStream setBinaryStream(long startPosition) 1.4
   返回一个输出流,用于从给定位置开始写入该BLOB。

#### API java.sql.Clob

- long length()
   获取该 CLOB 中的字符总数。
- String getSubString(long startPosition, long length)
   获取该 CLOB 中给定范围的字符。
- Reader getCharacterStream()
- Reader getCharacterStream(long startPosition, long length)
   返回一个读入器(而不是流),用于读取 CLOB 中全部或给定范围的数据。
- Writer setCharacterStream(long startPosition)
   返回一个写出器(而不是流),用于从给定位置开始写入该CLOB。

#### API java.sql.Connection

- Blob createBlob() 6
- Clob createClob() 6 创建一个空的 BLOB 或 CLOB。

#### 5.5.3 SQL 转义

"转义"语法是各种数据库普遍支持的特性,但是数据库使用的是与数据库相关的语法变体,因此,将转义语法转译为特定数据库的语法是 JDBC 驱动程序的任务之一。

转义主要用于下列场景:

- 日期和时间字面常量
- 调用标量函数
- 调用存储过程
- 外连接
- 在 LIKE 子句中的转义字符

日期和时间字面常量随数据库的不同而变化很大。要嵌入日期或时间字面常量,需要按照 ISO 8601 格式(http://www.cl.cam.ac.uk/~mgk25/iso-time.html) 指定它的值,之后驱动程序会将其转译为本地格式。应该使用 d、t、ts 来表示 DATE、TIME 和 TIMESTAMP 值:

```
{d '2008-01-24'}
{t '23:59:59'}
{ts '2008-01-24 23:59:59.999'}
```

标量函数(scalar function)是指仅返回单个值的函数。在数据库中包含大量的函数,但是不同的数据库中这些函数名存在着差异。JDBC 规范提供了标准的名字,并将其转译为数据库相关的名字。要调用函数,需要像下面这样嵌入标准的函数名和参数:

```
{fn left(?, 20)}
{fn user()}
```

在 JDBC 规范中可以找到它支持的函数名的完整列表。

两个表的外连接(outer join)并不要求每个表的所有行都要根据连接条件进行匹配,例如,假设有如下的查询:

```
SELECT * FROM {oj Books LEFT OUTER JOIN Publishers
ON Books.Publisher_Id = Publisher.Publisher_Id}
```

这个查询的执行结果中将包含有 Publisher\_Id 在 Publishers 表中没有任何匹配的书, 其中, Publisher\_ID 为 NULL 值的行, 就表示不存在任何匹配。如果使用 RIGHT OUTER JOIN, 就会囊括没有任何匹配图书的出版商, 而使用 FULL OUTER JOIN 可以同时返回这两类没有任何匹配的信息。由于并非所有的数据库对于这些连接都使用标准的写法, 因此需要使用转义语法。

最后一种情况,\_和%字符在 LIKE 子句中具有特殊含义,用来匹配一个字符或一个字符 序列。目前并不存在任何在字面上使用它们的标准方式,所以如果想要匹配所有包含\_字符 的字符串,就必须使用下面的结构:

```
. . . WHERE ? LIKE %!_% {escape '!'}
```

这里我们将!定义为转义字符,而!\_组合表示字面常量下划线。

存储过程(stored procedure)是在数据库中执行的用数据库相关的语言编写的过程。要调用存储过程,需要使用 call 转义命令。在存储过程没有任何参数时,可以不用加上括号。另外,应该用 = 来捕获存储过程的返回值:

```
{call PROC1(?, ?)}
{call PROC2}
{call ? = PROC3(?)}
```

你需要使用 CallableStatement 接口执行存储过程,设置所有输入参数,并指定所有输出的类型。

```
CallableStatement stat = conn.prepareCall("{call PROC4(?, ?)}")
stat.setInt(1, id);
stat.registerOutParameter(2, java.sql.Types.VARCHAR);
stat.execute();
String name = stat.getString(2);
```

#### 5.5.4 多结果集

在执行存储过程,或者在使用允许在单个查询中提交多个 SELECT 语句的数据库时,一个查询有可能会返回多个结果集。下面是获取所有结果集的步骤:

- 1. 使用 execute 方法来执行 SQL 语句。
- 2. 获取第一个结果集或更新计数。
- 3. 重复调用 getMoreResults 方法以移动到下一个结果集。
- 4. 当不存在更多的结果集或更新计数时, 完成操作。

如果由多结果集构成的链中的下一项是结果集, execute 和 getMoreResults 方法将返回 true, 而如果在链中的下一项不是更新计数, getUpdateCount 方法将返回 -1。

下面的循环可以遍历所有的结果:

```
boolean isResult = stat.execute(command);
boolean done = false;
while (!done)
{
    if (isResult)
    {
        ResultSet result = stat.getResultSet();
        do something with result
    }
    else
    {
        int updateCount = stat.getUpdateCount();
        if (updateCount >= 0)
            do something with updateCount
        else
            done = true;
    }
    if (!done) isResult = stat.getMoreResults();
}
```

#### API java.sql.Statement

- boolean getMoreResults()
- boolean getMoreResults(int current)
   获取该语句的下一个结果集, Current 参数是 CLOSE\_CURRENT\_RESULT(默认值), KEEP\_CURRENT\_RESULT或 CLOSE\_ALL\_RESULTS之一。如果存在下一个结果集,并且它确实是一个结果集,则返回 true。

#### 5.5.5 获取自动生成的键

大多数数据库都支持某种在数据库中对行自动编号的机制。但是,不同的提供商所提供的机制之间存在着很大的差异,而这些自动编号的值经常用作主键。尽管 JDBC 没有提供独立于提供商的自动生成键的解决方案,但是它提供了获取自动生成键的有效途径。当我们向数据表中插入一个新行,且其键自动生成时,可以用下面的代码来获取这个键:

```
stat.executeUpdate(insertStatement, Statement.RETURN_GENERATED_KEYS);
ResultSet rs = stat.getGeneratedKeys();\nif (rs.next())
{
   int key = rs.getInt(1);
   ...
}
```

#### API java.sql.Statement

- boolean execute(String statement, int autogenerated) 1.4
- int executeUpdate(String statement, int autogenerated) 1.4
  像前面描述的那样执行给定的 SQL 语句,如果 autogenerated 被设置为 Statement. RETURN\_GENERATED KEYS,并且该语句是一条 INSERT 语句,那么第一列中就是自动生成的键。

#### 5.6 可滚动和可更新的结果集

我们前面已经介绍过,使用 ResultSet 接口中的 next 方法可以迭代遍历结果集中的所有行。对于一个只需要分析数据的程序来说,这显然已经足够了。但是,如果是用于展示一张表或查询结果的可视化数据显示(参见图 5-4),我们通常会希望用户可以在结果集上前后移动。对于可滚动结果集而言,我们可以在其中向前或向后移动,甚至可以跳到任意位置。

另外,一旦向用户显示了结果集中的内容,他们就可能希望编辑这些内容。在可更新的结果集中,可以以编程方式来更新其中的项,使得数据库可以自动更新数据。我们将在下面的小节中讨论这些功能。

#### 5.6.1 可滚动的结果集

默认情况下,结果集是不可滚动和不可更新的。为了从查询中获取可滚动的结果集,必须使用下面的方法得到一个不同的 Statement 对象:

Statement stat = conn.createStatement(type, concurrency);

如果要获得预备语句, 请调用下面的方法:

PreparedStatement stat = conn.prepareStatement(command, type, concurrency);

表 5-6 和表 5-7 列出了 type 和 concurrency 的所有可能值,可以有以下几种选择:

- 是否希望结果集是可滚动的?如果不需要,则使用 ResultSet.TYPE\_FORWARD\_ONLY。
- 如果结果集是可滚动的,且数据库在查询生成结果集之后发生了变化,那么是否希望结果集反映出这些变化?(在我们的讨论中,我们假设将可滚动的结果集设置为

ResultSet.TYPE\_SCROLL\_INSENSITIVE。这个设置将使结果集"感应"不到查询结束后出现的数据库变化。)

• 是否希望通过编辑结果集就可以更新数据库?(详细说明请参见下一节内容。)

| 表 5-6 | ResultSet | 类的tv | /pe 值 |
|-------|-----------|------|-------|
|-------|-----------|------|-------|

| 值                       | 解释                  |
|-------------------------|---------------------|
| TYPE_FORWARD_ONLY       | 结果集不能滚动 (默认值)       |
| TYPE_SCROLL_INSENSITIVE | 结果集可以滚动, 但对数据库变化不敏感 |
| TYPE_SCROLL_SENSITIVE   | 结果集可以滚动,且对数据库变化敏感   |

表 5-7 ResultSet 类的 concurrency 值

| 值                | 解释                |
|------------------|-------------------|
| CONCUR_READ_ONLY | 结果集不能用于更新数据库(默认值) |
| CONCUR_UPDATABLE | 结果集可以用于更新数据库      |

例如,如果只想滚动遍历结果集,而不想编辑它的数据,那么可以使用以下语句。

Statement stat = conn.createStatement(
 ResultSet.TYPE SCROLL INSENSITIVE, ResultSet.CONCUR READ ONLY);

现在,通过调用以下方法获得的所有结果集都将是可滚动的。

ResultSet rs = stat.executeQuery(query);

可滚动的结果集有一个游标, 用以指示当前位置。

注释:并非所有的数据库驱动程序都支持可滚动和可更新的结果集。(使用 Database-MetaData 接口中的 supportsResultSetType 和 supportsResultSetConcurrency 方法,我们可以获知在使用特定的驱动程序时,某个数据库究竟支持哪些结果集类型以及哪些并发模式。)即便是数据库支持所有的结果集模式,某个特定的查询也可能无法产生带有所要求的所有属性的结果集。(例如,一个复杂查询的结果集就有可能是不可更新的结果集。)在这种情况下,executeQuery 方法将返回一个功能较少的 ResultSet 对象,并添加一个 SQLWarning 到连接对象中。(参见 5.4.3 节有关如何获取警告信息的内容)或者,也可以使用 ResultSet 接口中的 getType 和 getConcurrency 方法查看结果集实际支持的模式。如果不检查结果集的功能就发起一个不支持的操作,比如对不可滚动的结果集调用 previous 方法,那么该操作将抛出一个 SQLException 异常。

在结果集上滚动是非常简单的, 可以使用

if (rs.previous()) . . .;

向后滚动。如果游标位于一个实际的行上,那么该方法将返回 true;如果游标位于第一行之前,那么返回 false。

可以使用以下调用将游标向后或向前移动多行:

rs.relative(n);

如果n为正数,游标将向前移动。如果n为负数,游标将向后移动。如果n为 0,那么调用该方法将不起任何作用。如果试图将游标移动到当前行集的范围之外,即根据n值的正负号,游标需要被设置在最后一行之后或第一行之前,那么,该方法将返回 false,且不移动游标。如果游标位于一个实际的行上,那么该方法将返回 true。

或者,还可以将游标设置到指定的行号上:

rs.absolute(n);

调用以下方法将返回当前行的行号:

int currentRow = rs.getRow();

结果集中第一行的行号为 1。如果返回值为 0,那么游标当前不在任何行上,它要么位于第一行之前,要么位于最后一行之后。

first、last、beforeFirst 和 afterLast 这些简便方法用于将游标移动到第一行、最后一行、第一行之前或最后一行之后。

最后,isFirst、isLast、isBeforeFirst 和 isAfterLast 用于测试游标是否位于这些特殊位置上。 使用可滚动的结果集是非常简单的,将查询数据放入缓存中的复杂工作是由数据库驱动程序在后台完成的。

#### 5.6.2 可更新的结果集

如果希望编辑结果集中的数据,并且将结果集上的数据变更自动反映到数据库中,那么就必须使用可更新的结果集。可更新的结果集并非必须是可滚动的,但如果将数据展现给用户去编辑,那么通常也会希望结果集是可滚动的。

如果要获得可更新的结果集,应该使用以下方法创建一条语句:

Statement stat = conn.createStatement(
 ResultSet.TYPE\_SCROLL\_INSENSITIVE, ResultSet.CONCUR\_UPDATABLE);

这样,调用 executeQuery 方法返回的结果集就将是可更新的结果集。

註釋:并非所有的查询都会返回可更新的结果集。如果查询涉及多个表的连接操作,那么它所产生的结果集将可能是不可更新的。如果查询只涉及一个表,或者在查询时是使用主键连接多个表的,那么它所产生的结果集将是可更新的结果集。可以调用ResultSet接口中的getConcurrency方法来确定结果集是否是可更新的。

例如,假设想提高某些图书的价格,但是在执行 UPDATE 语句时又没有一个简单的提价标准。此时,就可以根据任意设定的条件,迭代遍历所有的图书并更新它们的价格。

```
String query = "SELECT * FROM Books";
ResultSet rs = stat.executeQuery(query);
while (rs.next())
{
   if (. . .)
   {
      double increase = . . .;
      double price = rs.getDouble("Price");
```

```
rs.updateDouble("Price", price + increase);
rs.updateRow(); // make sure to call updateRow after updating fields
}
```

所有对应于 SQL 类型的数据类型都配有 updateXxx 方法,比如 updateDouble、updateString 等。与 getXxx 方法相同,在使用 updateXxx 方法时必须指定列的名称或序号,然后给该字段设置新的值。

直 注释:在使用第一个参数为列序号的 updateXxx 方法时,请注意这里的列序号指的是该列在结果集中的序号。它的值可以与数据库中的列序号不同。

updateXxx 方法改变的只是结果集中的行值,而非数据库中的值。当更新完行中的字段值后,必须调用 updateRow 方法,这个方法将当前行中的所有更新信息发送给数据库。如果没有调用 updateRow 方法就将游标移动到其他行上,那么对此行所做的所有更新都将被丢弃,而且永远也不会被传递给数据库。还可以调用 cancelRowUpdates 方法来取消对当前行的更新。

我们在前面的例子中已经介绍过如何修改一个现有的行。如果想在数据库中添加一条新的记录,首先需要使用 moveToInsertRow 方法将游标移动到特定的位置,我们称之为插入行 (insert row)。然后,调用 updateXxx 方法在插入行的位置上创建一个新的行。在上述操作全部完成之后,还需要调用 insertRow 方法将新建的行发送给数据库。完成插入操作后,再调用 moveToUrrentRow 方法将游标移回到调用 moveToInsertRow 方法之前的位置。下面是一段示例程序:

```
rs.moveToInsertRow();
rs.updateString("Title", title);
rs.updateString("ISBN", isbn);
rs.updateString("Publisher_Id", pubid);
rs.updateDouble("Price", price);
rs.insertRow();
rs.moveToCurrentRow();
```

请注意, 你无法控制在结果集或数据库中添加新数据的位置。

对于在插入行中没有指定值的列,将被设置为 SQL 的 NULL。但是,如果这个列有 NOT NULL 约束,那么将会抛出异常,而这一行也无法插入。

最后需要说明的是, 你可以使用以下方法删除游标所指的行。

```
rs.deleteRow();
```

deleteRow方法会立即将该行从结果集和数据库中删除。

ResultSet 接口中的 updateRow、insertRow 和 deleteRow 方法的执行效果等同于 SQL 命令中的 UPDATE、INSERT 和 DELETE。不过,习惯于 Java 编程语言的程序员通常会觉得使用结果集来操控数据库要比使用 SQL 语句自然得多。

● 警告:如果不小心处理的话,就很有可能在使用可更新的结果集时编写出非常低效的代码。执行 UPDATE 语句,要比建立一个查询,然后一边遍历一边修改数据显得高效得多。对于用户能够任意修改数据的交互式程序来说,使用可更新的结果集是非常有意义的。但是相对于大多数通过程序进行修改的情况,使用 SQL 的 UPDATE 语句更合适一些。

注释: JDBC 2 对结果集做了进一步的改进,例如,如果数据被其他的并发数据库连接所修改,那么它可以用最新的数据来更新结果集。JDBC 3 添加了另一种优化,可以指定结果集在事务提交时的行为。但是,这些高级特性超出了本章的范围。我们推荐你参考 Maydene Fisher、Jon Ellis 和 Jonathan Bruce 所著的 JDBC API Tutorial and Reference, Third Edition (Addison-Wesley 出版社 2003 年出版)和 JDBC 规范,以了解更多的信息。

#### API java.sql.Connection

- Statement createStatement(int type, int concurrency) 1.2
- PreparedStatement prepareStatement(String command, int type, int concurrency) 1.2 创建一个语句或预备语句,且该语句可以产生指定类型和并发模式的结果集。type 参数是 ResultSet 接口中的下述常量之一: TYPE\_FORWARD\_ONLY、TYPE\_SCROLL\_INSENSITIVE 或者 TYPE\_SCROLL\_SENSITIVE, concurrency 参数是 ResultSet 接口中的下述常量之一: CONCUR READ ONLY 或者 CONCUR UPDATABLE

#### API java.sql.ResultSet

- int getType() 1.2 返回结果集的类型。返回值为以下常量之一: TYPE\_FORWARD\_ONLY、TYPE\_SCROLL\_INSENSITIVE或 TYPE SCROLL SENSITIVE。
- int getConcurrency() 1.2
   返回结果集的并发设置。返回值为以下常量之一: CONCUR\_READ\_ONLY或 CONCUR\_UPDATABLE
- boolean previous() 1.2
   将游标移动到前一行。如果游标位于某一行上,则返回 true;如果游标位于第一行之前的位置,则返回 false。
- int getRow() 1.2 得到当前行的序号。所有行从1开始编号。
- boolean absolute(int r) 1.2
   移动游标到第 r 行。如果游标位于某一行上,则返回 true。
- boolean relative(int d) 1.2
   将游标移动 d 行。如果 d 为负数,则游标向后移动。如果游标位于某一行上,则返回 true。
- boolean first() 1.2
- boolean last() 1.2 移动游标到第一行或最后一行。如果游标位于某一行上,则返回 true。
- void beforeFirst() 1.2
- void afterLast() 1.2

移动游标到第一行之前或最后一行之后的位置。

- boolean isFirst() 1.2
- boolean isLast() 1.2 测试游标是否在第一行或最后一行。
- boolean isBeforeFirst() 1.2
- boolean isAfterLast() 1.2 测试游标是否在第一行之前或最后一行之后的位置。
- void moveToInsertRow() 1.2
   移动游标到插入行。插入行是一个特殊的行,可以在该行上使用 updateXxx 和 insertRow 方法来插入新数据。
- void moveToCurrentRow() 1.2
   将游标从插入行移回到调用 moveToInsertRow 方法之前它所在的那一行。
- void insertRow() 1.2 将插入行上的内容插入到数据库和结果集中。
- void deleteRow() 1.2
   从数据库和结果集中删除当前行。
- void updateXxx(int column, Xxx data) 1.2
- void updateXxx(String columnName, Xxx data) 1.2
   (Xxx 指数据类型, 比如 int、double、String、Date 等) 更新结果集中当前行上的某个字段值。
- void updateRow() 1.2
   将当前行的更新信息发送到数据库。
- void cancelRowUpdates() 1.2
   撤销对当前行的更新。

#### API java.sql.DatabaseMetaData

- boolean supportsResultSetType(int type) 1.2
   如果数据库支持给定类型的结果集,则返回 true。type 是 ResultSet 接口中的常量之一: TYPE FORWARD ONLY、TYPE SCROLL INSENSITIVE或者 TYPE SCROLL SENSITIVE。
- boolean supportsResultSetConcurrency(int type, int concurrency) 1.2 如果数据库支持给定类型和并发模式的结果集,则返回 true。type 参数是 ResultSet 接口中的下述常量之一: TYPE\_FORWARD\_ONLY、TYPE\_SCROLL\_INSENSITIVE 或者 TYPE\_SCROLL\_SENSITIVE。concurrency 是 ResultSet 接口中的下述常量之一: CONCUR\_READ\_ONL 或者 CONCUR\_UPDATABLE。

#### 5.7 行集

可滚动的结果集虽然功能强大,却有一个重要的缺陷:在与用户的整个交互过程中,必

须始终与数据库保持连接。用户也许会离开电脑旁很长一段时间,而在此期间却始终占有着数据库连接。这种方式存在很大的问题,因为数据库连接属于稀有资源。在这种情况下,我们可以使用行集。RowSet 接口扩展自 ResultSet 接口,却不需要始终保持与数据库的连接。

行集还适用于将查询结果移动到复杂应用的其他层,或者是诸如手机之类的其他设备中。你可能永远都不会考虑移动一个结果集,因为它的数据结构可能非常庞大,且依赖于数据库连接。

#### 5.7.1 构建行集

以下为 javax.sql.rowset 包提供的接口,它们都扩展了 RowSet 接口:

- CachedRowSet 允许在断开连接的状态下执行相关操作。关于被缓存的行集我们将在下一节中讨论。
- WebRowSet 对象代表了一个被缓存的行集,该行集可以保存为 XML 文件。该文件可以 移动到 Web 应用的其他层中,只要在该层中使用另一个 WebRowSet 对象重新打开该文件即可。
- FilteredRowSet 和 JoinRowSet 接口支持对行集的轻量级操作,它们等同于 SQL 中的 SELECT 和 JOIN 操作。这两个接口的操作对象是存储在行集中的数据,因此运行时无 须建立数据库连接。
- JdbcRowSet 是 ResultSet 接口的一个瘦包装器。它在 RowSet 接口中添加了一些有用的方法。
   要想获取被缓存的行集,可以执行下面的调用:

RowSetFactory factory = RowSetProvider.newFactory();
CachedRowSet crs = factory.createCachedRowSet();

获取其他行集类型的对象也有类似的方法。

#### 5.7.2 被缓存的行集

一个被缓存的行集中包含了一个结果集中所有的数据。CachedRowSet 是 ResultSet 接口的子接口,所以你完全可以像使用结果集一样来使用被缓存的行集。被缓存的行集有一个非常重要的优点:断开数据库连接后仍然可以使用行集。你将在程序清单 5-4 的示例程序中看到,这种做法大大简化了交互式应用的实现。在执行每个用户命令时,我们只需打开数据库连接、执行查询操作、将查询结果放入被缓存的行集,然后关闭数据库连接即可。

我们甚至可以修改被缓存的行集中的数据。当然,这些修改不会立即反馈到数据库中。相反,必须发起一个显式的请求,以便让数据库真正接受所有修改。此时 CachedRowSet 类会重新连接到数据库,并通过执行 SQL 语句向数据库中写入所有修改后的数据。

可以使用一个结果集来填充 CachedRowSet 对象:

ResultSet result = . . .;
RowSetFactory factory = RowSetProvider.newFactory();
CachedRowSet crs = factory.createCachedRowSet();
crs.populate(result);
conn.close(); // now OK to close the database connection

或者,也可以让 CachedRowSet 对象自动建立一个数据库连接。首先,设置数据库参数:

```
crs.setURL("jdbc:derby://localhost:1527/COREJAVA");
crs.setUsername("dbuser");
crs.setPassword("secret");
```

然后,设置查询语句和所有参数:

```
crs.setCommand("SELECT * FROM Books WHERE Publisher_ID = ?");
crs.setString(1, publisherId);
```

最后, 将查询结果填充到行集中:

```
crs.execute();
```

这个方法调用会建立数据库连接、执行查询操作、填充行集,最后断开连接。

如果查询结果非常大,那我们肯定不想将其全部放入行集中。毕竟,用户可能只是想浏览其中的几行而已。在这种情况下,可以指定每一页的尺寸:

```
CachedRowSet crs = . . .;
crs.setCommand(command);
crs.setPageSize(20);
. . .
crs.execute();
```

现在就能只获取20行了。要获取下一批数据,可以调用:

```
crs.nextPage();
```

可以使用与结果集中相同的方法来查看和修改行集中的数据。如果修改了行集中的内容,那么必须调用以下方法将修改写回到数据库中:

```
crs.acceptChanges(conn);
```

或

crs.acceptChanges();

只有在行集中设置了连接数据库所需的信息(如 URL、用户名和密码)时,上述第二个方法调用才会有效。

在 5.6.2 节中, 我们曾经介绍过, 并非所有的结果集都是可更新的。同样, 如果一个行集包含的是复杂查询的查询结果, 那么我们就无法将对该行集数据的修改写回到数据库中。不过, 如果行集上的数据都来自同一张数据库表, 我们就可以安全地写回数据。

● 警告:如果是使用结果集来填充行集,那么行集就无从获知需要更新数据的数据库表名。此时,必须调用 setTable 方法来设置表名称。

另一个导致问题复杂化的情况是:在填充了行集之后,数据库中的数据发生了改变,这显然容易产生数据不一致性。为了解决这个问题,参考实现会首先检查行集中的原始值(即,修改前的值)是否与数据库中的当前值一致。如果一致,那么修改后的值将覆盖数据库中的当前值。否则,将抛出 SyncProviderException 异常,且不向数据库写回任何值。在实现行集接口时其他实现也可以采用不同的同步策略。

#### *奶| javax.sql.RowSet*

- *• String getURLO*
- *• void setURL(String url) 取或 数据库 URL。*
- *• String getUsernameO*
- *• void setUsername(String username) 取或 接数据库所 户名。*
- *• String getPasswordO*
- *• void setPassword(String password) 取或设置连接数据库所需的密 。*
- *• String getCo\_and()*
- *• void setCo\_and(String command) 取或设置向行集中填充数据时需要执行的命令。*

*接 必 事先 定URL、 户名和密 。*

*• void execute!) 执 使 setCo刪and方法 句 来填充 。为了使 动 器可以 得*

#### *Anj javax. sql. rowset. CachedRowSet*

- *• void execute(Connection conn) 执 使 setCo and方法 句 来填充 。 方法使 定 接 并 负责关 它。*
- *• void populate(ResultSet result) 将指定 果 中 数据填充到 存 中。*
- *• String getTableNameO*
- *• void setTableName(String tableName) 取或 数据库 名 填充 存 时所 数据来 。*
- *• int getPageSizeO*
- *• void setPageSize(int size) 取和 尺寸。*
- *• boolean nextPageO*
- *• boolean previousPageO 加 下一 或上一 如果 加 存在 则 回true。*
- *• void acceptChangesO*
- *• void acceptChanges(Connection conn)*

*新 接数据库 并写回 中修改 数据。如果因为数据库中 数据已 修改 导 无法写回 中 数据 方法可 会抛出SyncProviderException异常。*

#### *<sup>a</sup>«] javax.sql.rowset.RowSetProvider*

*• static RowSetFactory newFactoryO 创建一个行集工厂。*

#### *j avax.sql.rowset.RowSetFactory*

- *• CachedRowSet createCachedRowSet()*
- *• FilteredRowSet createFilteredRowSet()*
- *• JdbcRowSet createJdbcRowSetO*
- *• JoinRowSet createJoinRowSetO*
- *• WebRowSet createWebRowSetO 创建一个指定 型 。*

## *5.8元数据*

*在前几 中 我们介 了如何填充、查 和更新数据库 。其实 JDBC 可以提供关于数 据库及其表结构的详细信息。例如 可以 取 某个数据库 所有 构成 列 或 是 某 个 中所有列 名 及其数据 型构成 列 。如果是在开发业务应 时使 事先定义好 数 据库 么数据库 构和 信息就不是 常有 了。毕 在 数据库 时 就已 了它 们的结构。但是 对于 些 写数据库工具 序员来 数据库的结构信息却是极其有用的。*

*在SQL中 描 数据库或其 成 分 数据 为元数据(区别于 些存在数据库中 实 数据)。我们可以 得三 元数据 关于数据库 元数据、关于 果 元数据以及关于 备 句参数 元数据。*

*如果 了 数据库 更多信息 可以从数据库 接中 取一个DatabaseMetaData对 。*

*DatabaseMetaData meta = conn.getMetaDataO;*

*在就可以 取某些元数据了。例如*

*ResultSet mrs <sup>=</sup> meta.getTabl.es(null, null, null, new St ring[] { "TABLE" });*

*将 回一个包含所有数据库 信息 果 (如果 了 方法 其他参数 参 本 末 尾 API 明)。*

*果 中 每一 包含了数据库中一张 信息 其中 三列是 名 。 (同样 如果 了 其他列 信息 参 API 明。)下 循 可以 取所有 名*

*while (mrs.nextO) tableNames.addItem(mrs.getString(3));*

*数据库元数据 有 二个 应 。数据库是 常复杂 SQL标准为数据库 多样性 提供了很大 。DatabaseMetaData接口中有上 个方法可以 于査 数据库 关信息 包括一些使 奇特的名字进行调用的方法 如*

*meta•supportsCatalogsInPrivilegeDefinitions()*

*和*

*meta • nuUPlusNonNulUsNuU()*

*显然 些方法主 是 对有 殊 求的髙级用户 尤其是 些 写涉及多个数 据库且具有 可 植性 代 人员。*

*DatabaseMetaData接口 于提供有关数据库 数据 二个元数据接口 ResultSetMetaData 则 于提供 果 关信息。每当 査 得到一个 果 时 我们 可以 取 果 列数以及每一列 名 、 型和字段宽度。下 是一个典型 循*

```
ResultSet rs = stat.executeQuery("SELECT FROM ・ + tableName):
ResultSetMetaData meta = rs.getMetaDataO;
for (int i = 1; i <= meta.getColuanCountO; i++)
{
   String columnName = meta.getColunnLabel(i);
   int columnwidth ■ meta.getColuinDisplaySize(i);
   _ 參 參
}
```

*在 一 中 我们将介 如何 写一个 单 数据库工具 序清单5-4中 序 使 元数据来浏 数据库中 所有 序 展 了如何使 存 。*

#### *序清单 5-4 view/ViewDB.java*

```
1 package view;
2
3import java.awt.*;
4 import java.awt.event.*;
5 import java.io.*;
6 import java.nio.charset.*;
7 import java.nio.file.*;
8 import java.sql.*;
9 import java.util.*;
le
11 import javax.sqU*;
12 import javax.sql.rowset.*;
b import javax.swing.*;
14
15 /**
is * This program uses metadata to display arbitrary tables in a database.
17 * ^version 1.35 2921-06-17
is * ^author Cay Horstmann
19 /
2e public class ViewOB
n {
22 public static void main(String!] args)
» {
24 EventQueue.invokeLater(()->
25 {
26 var frame = new ViewOBFrameO;
27 frame.setTitle{・ViewDB");
28 frame.setDefaultCloseOperation(JFrame・ EXIT_ON_CLOSE);
29 frame.setVisible(true);
```

```
36
31
32
13
36
37
38
39
4«
41
42
43
44
45
46
47
48
49
56
51
52
53
54
55
56
57
58
59
69
61
62
63
M
65
66
67
68
69
76
72
73
74
75
76
77
78
79
Sfi
81
82
83
84
   /**
      The frame that holds the data panel and the navigation buttons.
   class ViewDBFrame extends JFrame
   {
       private JButton previousButton;
       private JButton nextButton;
       private JButton deleteButton;
       private JButton saveButton;
       private DataPanel dataPanel;
       private Component scrollPane;
       private JConboBox<String> tableNames;
       private Properties props;
       private CachedRowSet crs;
       private Connection conn;
       public ViewDBFrameO
       {
          tableNames = new JComboBox<String>();
              readDatabaseProperties();
              conn = getConnectionO;
             DatabaseMetaData meta = conn.getMetaData();
              try (ResultSet mrs = meta.getTables(null, null, null, new String!] { "TABLE" }))
              {
                 while (mrs.nextO)
                    tableNames.addItem(mrs.getString(3));
          }
          catch (SQLException e)
          {
              for (Throwable t : e)
                 t.printStackTrace();
          }
          catch (IOException e)
          {
              ex.printStackTraceO;
          tableNames•addActionListener(
              event -> showTable((String) tableNames.getSelectedltemf), conn));
          add(tableNames, BorderLayout.NORTH);
          addWindowListener(new WindowAdapterf)
              {
                 public void windowclosing(WindowEvent event)
                        if (conn != null) conn.closeO;
```

```
catch (SQLException e)
86
87
                   {
                      for (Throwable t : e)
                         t.printStackTrace();
89
98
91
            });
92
93
         var buttonPanel = new JPanel();
94
         add(buttonPanel, BorderLayout.SOUTH);
95
96
         previousButton = new JButton("Previous");
97
         previousButton.addActionListener(event -> showPreviousRow());
98
         buttonPanel.add(previousButton);
99
188
         nextButton = new JButton("Next");
191
         nextButton.addActionListener(event -> showNextRow());
192
         buttonPanel.add(nextButton);
103
         deleteButton = new JButton("Delete");
105
         deleteButton.addActionListener(event -> deleteRow());
186
         buttonPanel.add(deleteButton);
100
         saveButton = new JButton("Save");
109
          saveButton.addActionListener(event -> saveChanges());
          buttonPanel.add(saveButton);
111
          if (tableNames.getItemCount() > θ)
112
             showTable(tableNames.getItemAt(0), conn);
113
114
115
116
       * Prepares the text fields for showing a new table, and shows the first row.
117
       * @param tableName the name of the table to display
        * @param conn the database connection
119
128
      public void showTable(String tableName, Connection conn)
121
122
          try (Statement stat = conn.createStatement():
123
                ResultSet result = stat.executeQuery("SELECT * FROM " + tableName))
125
             // get result set
126
             // copy into cached row set
128
             RowSetFactory factory = RowSetProvider.newFactory();
129
             crs = factory.createCachedRowSet();
             crs.setTableName(tableName);
131
             crs.populate(result);
132
             if (scrollPane != null) remove(scrollPane);
             dataPanel = new DataPanel(crs);
135
             scrollPane = new JScrollPane(dataPanel);
136
             add(scrollPane, BorderLayout.CENTER);
             pack();
138
             showNextRow():
139
```

```
140
          catch (SQLException e)
141
142
             for (Throwable t : e)
143
                t.printStackTrace();
144
145
      }
146
147
148
        * Moves to the previous table row.
149
158
      public void showPreviousRow()
151
152
          try
153
          {
154
             if (crs == null || crs.isFirst()) return;
155
             crs.previous();
156
             dataPanel.showRow(crs);
157
158
          catch (SQLException e)
159
169
              for (Throwable t : e)
161
                 t.printStackTrace();
162
163
164
165
166
        * Moves to the next table row.
167
168
       public void showNextRow()
169
170
171
          try
177
             if (crs == null || crs.isLast()) return;
173
              crs.next();
174
              dataPanel.showRow(crs);
175
176
          catch (SQLException e)
177
178
              for (Throwable t : e)
179
                 t.printStackTrace();
188
181
182
183
184
        * Deletes current table row.
185
186
       public void deleteRow()
187
188
          if (crs == null) return;
189
          new SwingWorker<Void, Void>()
198
191
              public Void doInBackground() throws SQLException
192
193
                 crs.deleteRow();
194
```

274

```
crs.acceptChanges(conn);
195
                if (crs.isAfterLast())
196
197
                   if (!crs.last()) crs = null;
                return null;
198
199
             public void done()
281
                dataPanel.showRow(crs):
282
263
          }.execute();
284
205
286
       * Saves all changes.
287
208
      public void saveChanges()
289
210
          if (crs == null) return;
211
          new SwingWorker<Void, Void>()
212
213
             public Void doInBackground() throws SQLException
214
             {
215
216
                dataPanel.setRow(crs);
                crs.acceptChanges(conn);
217
                return null;
21R
          }.execute();
228
221
222
      private void readDatabaseProperties() throws IOException
223
224
          props = new Properties();
225
          try (Reader in = Files.newBufferedReader(
226
                Path.of("database.properties"), StandardCharsets.UTF 8))
227
228
             props.load(in);
229
238
          String drivers = props.getProperty("jdbc.drivers");
231
          if (drivers != null) System.setProperty("jdbc.drivers", drivers);
232
233
234
       /**
235
        * Gets a connection from the properties specified in the file database.properties.
236
        * @return the database connection
237
238
       private Connection getConnection() throws SQLException
239
240
          String url = props.getProperty("jdbc.url");
241
          String username = props.getProperty("jdbc.username");
242
          String password = props.getProperty("jdbc.password");
243
244
          return DriverManager.getConnection(url, username, password);
245
246
247 }
248
249 /**
```

```
253 {
2M
255
256
257
258
259
2M
2€1
2€2
2€3
264
265
266
H7
268
269
279
271
272
273
274
275
276
277
278
279
286
281
282
283
284
285
286
287
2助
289
296
291
292
293
294
295
2%
297
298
299
3M
昶1
302
383
3M
25
251
252
    * This panel displays the contents of a result set.
    */
   class DataPanel extends JPanel
      private java.util,List<JTextField> fields;
        * Constructs the data panel.
            aram rs the result set whose contents this panel displays
      public DataPanel(RowSet rs) throws SQLException
       {
          fields = new ArrayListo()
          setLayout(new GridBagLayoutO);
          var gbc = new GridBagConstraintsO;
          gbc.gridwidth = 1;
          gbc.gridheight = 1;
          ResultSetMetaData rsnxl = rs.getMetaDataO;
          for (int i = 1; i <= rsnxi.getCol.umnCount();
          {
             gbc.gridy = i • 1;
             String columnName = rsmd.getColuranLabel(1);
             gbc.gridx = 0;
             gbc.anchor = GridBagConstraints.EAST;
             add (new JLabel(columnNaine), gbc);
              int columnwidth = rsmd.getColumnDisplaySize(i);
              var tb = new JTextField(columnWidth);
              if (!rsmd.getColumnClassName(i).equals("java.lang.String"))
                 tb.setEditable(false);
              fields.add(tb);
              gbc.gridx = 1;
              gbc.anchor = GridBagConstraints.WEST;
              add(tb, gbc);
        ' Shows a database row by populating all text fields with the column values.
        »/
       public void showRow(ResultSet rs)
              for (int i = 1; i <= fields.sized; i-H-)
                 String field = rs = null ?・" rs.getString(i);
                 JTextField tb = fields.get(i • 1);
                 tb.setText(field);
```

276

```
catch (SQLException e)
305
386
          {
             for (Throwable t : e)
307
                t.printStackTrace();
388
         }
309
310
311
312
       * Updates changed data into the current row of the row set.
313
314
      public void setRow(RowSet rs) throws SQLException
315
316
          for (int i = 1; i <= fields.size(); i++)
317
318
          {
             String field = rs.getString(i);
319
             JTextField tb = fields.get(i - 1);
328
             if (!field.equals(tb.getText()))
321
                rs.updateString(i, tb.getText());
322
323
          rs.updateRow();
324
       }
325
326 }
```

顶部的组合框用于显示数据库中的所有表。选中其中一个表,框中央就会显示出该表的所有字段名及其第一条记录的值,见图 5-6。点击 Next 和 Previous 按钮可以滚动遍历表中的所有记录,还可以删除一行或编辑行的值,点击 Save 按钮可以将各种修改保存到数据库中。

![](_page_69_Picture_3.jpeg)

图 5-6 ViewDB 应用程序

這一注释:许多数据库都配有复杂得多的工具,用于查看和编辑数据库表。如果你使用的数据库没有这样的工具,那么可以求助于DBeaver (https://dbeaver.io)或者SQuirreL (http://squirrel-sql.sourceforge.net)。这些程序可以查看任何JDBC数据库中的表。我们编写示例程序并非为了取代这些工具,而是为了向你演示如何编写工具来处理任意的数据库表。

#### API java.sql.Connection

DatabaseMetaData getMetaData()
 返回一个 DatabaseMetaData 对象,该对象封装了有关数据库连接的元数据。

#### *j ava.sql.DatabaseMetaData*

*• ResultSet getTables(String catalog, String schemapattern, String tableNamePattern, String types[])*

*回某个 录(catalog)巾所有 描 录必 匹 定 模式(schema)、 名字模式以及 型标准。(模式 于描 一 关 和 权 录描 是一 关 模式 些概念对 大型数据库 常 。)*

*catalog和schema参数可以为"" 于检索那些没有 录或模式的表。如果不想 录和模式 也可以将上 参数 为null。*

*types数 包含了所 型 名 常表类型有TABLE、VIEW、SYSTEM TABLE. GLOBAL TEMPORARY. LOCAL TEMPORARY. ALIAS <sup>和</sup> SYNONYM。如果 types <sup>为</sup> null,<sup>则</sup> 冋所 有 型的表。*

*回 果 共有5列 均为String 型。*

|   | 名           |             |
|---|-------------|-------------|
| 1 | TABLE_CAT   | 录(可以为null)  |
| 2 | TABLE_SCHEM | 模式(可以为null) |
| 3 | TABLE_NAME  | 名           |
| 4 | TABLETYPE   | 型           |
| 5 | REMARKS     | 关于<br>注     |

- *• int getJDBCMajorVersion()*
- *• int getJDBCMinorVersion()*

*回建 数据库 接 JDBC 动 序 主 本号和次 本号。例如 一个JDBC 4.3 <sup>动</sup> 序有一个主 本号4和一个次 本号3<sup>0</sup>*

- *• int getMaxConnections() 回可同时 接到数据库 最大并发 接数。*
- *• int getMaxStatementsO*

*回单个数据库 接允 同时打开 最大并发 句数。如果对允 打开的语句数 没 有 制或 不可 则 冋0。*

#### *奶| java.sql.ResultSet*

*• ResultSetMetaData getMetaDataO 回与当前ResultSet对 中 列 关 元数据。*

#### *java.sql.ResultSetMetaData*

- *• int getColumnCountO 回当前ResultSet对 中 列数。*
- *• int getColumnDisplaySize(int column) 回 定列序号 列 最大宽度。*

- String getColumnLabel(int column)
   返回该列所建议的名称。
- String getColumnName(int column)
   返回指定的列序号所对应的列名。

#### 5.9 事务

我们可以将一组语句构建成一个事务(transaction)。当所有语句都顺利执行之后,事务可以被提交(commit)。否则,如果其中某个语句遇到错误,那么事务将被回滚,就好像没有任何语句被执行过一样。

将多个语句组合成事务的主要原因是为了确保数据库完整性(database integrity)。例如,假设我们需要将钱从一个银行账号转账到另一个账号。此时,一个非常重要的问题就是我们必须同时将钱从一个账号取出并且存入另一个账号。如果在将钱存入其他账号之前系统发生崩溃,那么我们必须撤销取款操作。

如果将更新语句组合成一个事务,那么事务要么成功地执行所有操作并提交,要么在中间某个位置发生失败。在后面这种情况下,可以执行回滚(rollback)操作,数据库将自动撤销自上次提交事务以来的所有更新操作产生的影响。

#### 5.9.1 用 JDBC 对事务编程

默认情况下,数据库连接处于自动提交模式(autocommit mode),即每个 SQL 语句一旦被执行便被提交给数据库。一旦命令被提交,就无法对它进行回滚操作。在使用事务时,需要关闭这个默认值:

conn.setAutoCommit(false):

现在可以按照通常的方式创建一个语句对象:

Statement stat = conn.createStatement();

然后任意多次地调用 executeUpdate 方法:

```
\begin{array}{l} {\sf stat.executeUpdate}(command_1);\\ {\sf stat.executeUpdate}(command_2);\\ {\sf stat.executeUpdate}(command_3);\\ \end{array}
```

如果执行了所有命令之后没有出错,则调用 commit 方法:

conn.commit();

如果出现错误,则调用:

conn.rollback();

此时,程序将自动撤销自上次提交以来的所有语句。当事务被 SQLException 异常中断时,典型的办法就是发起回滚操作。

#### 5.9.2 保存点

在使用某些驱动程序时,使用保存点(save point)可以更细粒度地控制回滚操作。创建一个保存点意味着稍后只需返回到这个点,而非放弃整个事务。例如,

```
Statement stat = conn.createStatement(); // start transaction; rollback() goes here stat.executeUpdate(command1);
Savepoint svpt = conn.setSavepoint(); // set savepoint; rollback(svpt) goes here stat.executeUpdate(command2);
\nif (. . .) conn.rollback(svpt); // undo effect of command2
. . . . . . . . . . . . . . . . . . .
```

#### 5.9.3 批量更新

假设有一个程序需要执行许多 INSERT 语句,以便将数据填入数据库表中,此时可以使用批量更新的方法来提高程序性能。在使用批量更新(batch update)时,一个语句序列作为一批操作将同时被收集和提交。

**注释:** 使用 DatabaseMetaData 接口中的 supportsBatchUpdates 方法可以获知数据库是 否支持这种特性。

处于同一批中的语句可以是 INSERT、UPDATE 和 DELETE 等操作,也可以是数据库定义语句,如 CREATE TABLE 和 DROP TABLE。但是,在批量处理中添加 SELECT 语句会抛出异常(从概念上讲,批量处理中的 SELECT 语句没有意义,因为它会返回结果集,而并不更新数据库)。

为了执行批量处理,首先必须使用通常的办法创建一个 Statement 对象:

```
Statement stat = conn.createStatement();
```

现在,应该调用 addBatch 方法,而非 executeUpdate 方法:

```
String command = "CREATE TABLE . . ."
stat.addBatch(command);

while (. . .)
{
   command = "INSERT INTO . . . VALUES (" + . . . + ")";
   stat.addBatch(command);
}
```

#### 最后, 提交整个批量更新语句:

```
int[] counts = stat.executeBatch();
```

调用 executeBatch 方法将返回一个由所有提交的语句执行后受影响的行数构成的数组。 为了在批量模式下正确地处理错误,必须将批量执行的操作视为单个事务。如果批量更 *新在执 中失 么必 将它回滚到批 操作开始之前 态。*

*先 关 动提交模式 然后收 批 操作 执 并提交 操作 最后恢复最初 动提交模式*

```
boolean autoConnit = conn.getAutoConnit();
conn•setAutoCoomit(false);
Statement stat = conn.getStatement();
"keep calling stat.addBatch(..
stat.executeBatch();
conn.conmit(); conn.setAutoCoflnit(autoConnit);
```

#### *aw] java.sql.Connection*

- *• boolean getAutoCommitO*
- *• void setAutoCommit(boolean b) 取该连接中的自动提交模式 或将其设置为b。如果 动更新为true, 么所有 句将在执 束后 刻 提交。*
- *• void commit() 提交 上次提交以来所有执行过的语句。*
- *• void rollback() 撤 上次提交以来所有执 句所产 影响。*
- *• Savepoint setSavepoint() <sup>1</sup> <sup>4</sup>*
- *• Savepoint setSavepoint(String name) 一个匿名或具名 保存点。*
- *• void rollback(Savepoint svpt) 回滚到 定保存点。*
- *• void releaseSavepoint(Savepoint svpt) 放 定 保存点。*

#### *ah<sup>|</sup> java.sql.Savepoint*

- *• int getSavepointldO 取 匿名保存点 ID号。如果 保存点具有名字 则抛出一个SQLException异常<sup>c</sup>*
- *• String getSavepointName() 取 保存点 名 。如果 对 为匿名保存点 则抛出一个SQLException异常。*

#### *ar] java.sql.Statement*

- *• void addBatch(String command) 添加命令到 句当前 批 命令中。*
- *• int[] executeBatchO*
- *• long[] executeLargeBatch()*

执行当前批量更新中的所有命令。返回一个记录数的数组,其中每一个元素都对应一条语句,如果其值非负,则表示受该语句影响的行数;如果其值为 SUCCESS\_NO\_INFO,则表示该语句成功执行了,但没有提供任何行数;如果其值为 EXECUTE\_FAILED,则表示该语句执行失败了。

#### API java.sql.DatabaseMetaData

boolean supportsBatchUpdates() 1.2
 如果驱动程序支持批量更新,则返回 true。

#### 5.9.4 高级 SQL 类型

表 5-8 列举了 JDBC 支持的 SQL 数据类型以及它们在 Java 语言中对应的数据类型。

| SQL 数据类型                              | Java 数据类型            |
|---------------------------------------|----------------------|
| INTEGER 或 INT                         | int                  |
| SMALLINT                              | short                |
| NUMERIC(m,n), DECIMAL(m,n) 或 DEC(m,n) | java.math.BigDecimal |
| FLOAT(n)                              | double               |
| REAL                                  | float                |
| DOUBLE                                | double               |
| CHARACTER(n) 或 CHAR(n)                | String               |
| VARCHAR(n), LONG VARCHAR              | String               |
| BOOLEAN                               | boolean              |
| DATE                                  | java.sql.Date        |
| TIME                                  | java.sql.Time        |
| TIMESTAMP                             | java.sql.Timestamp   |
| BLOB                                  | java.sql.Blob        |
| CLOB                                  | java.sql.Clob        |
| ARRAY                                 | java.sql.Array       |
| ROWID                                 | java.sql.RowId       |
| NCHAR(n), NVARCHAR(n), LONG NVARCHAR  | String               |
| NCLOB                                 | java.sql.NClob       |
| SQLXML                                | java.sql.SQLXML      |

表 5-8 SQL 数据类型及其对应的 Java 类型

SQL ARRAY (SQL 数组)指的是值的序列。例如,Student 表中通常都会有一个 Scores 列,这个列就应该是 ARRAY OF INTEGER (整数数组)。getArray 方法返回一个接口类型为 java. sql.Array 的对象,该接口中有许多方法可以用来获取数据值。

从数据库中获得一个 LOB 或数组并不等于获取了它的实际内容,只有在访问具体的值

282

时它们才会从数据库中被读取出来。这对改善性能非常有好处,因为通常这些数据的数据量都非常大。

某些数据库支持描述行位置的 ROWID 值,这样就可以非常快捷地获取某一行值。JDBC 4 引入了 java.sql.RowId 接口,并提供了用于在查询中提供行 ID,以及从结果中获取该值的方法。

国家属性字符串(NCHAR 及其变体)按照本地字符编码机制存储字符串,并使用本地排序惯例对这些字符串进行排序。JDBC 4 提供了方法,用于在查询和结果中进行 Java 的 String 对象和国家属性字符串之间的双向转换。

有些数据库可以存储用户自定义的结构化类型。JDBC 3 提供了一种机制用于将 SQL 结构化类型自动映射成 Java 对象。

有些数据库提供用于 XML 数据的本地存储。JDBC 4 引入了 SQLXML 接口,它可以在内部的 XML 表示和 DOM 的 Source/Result 接口或二进制流之间起到中介作用。请查看 SQLXML 类的 API 文档以了解详细信息。

我们不再更深入地讨论这些高级 SQL 类型了,你可以在 JDBC API Tutorial and Reference 和 JDBC 规范中找到更多有关这些主题的信息。

#### 5.10 Web 与企业应用中的连接管理

我们在前面几节中曾经介绍过,使用 database.properties 文件可以对数据库连接进行非常简单的设置。这种方法适用于小型的测试程序,但是不适用于规模较大的应用。

在Web或企业环境中部署JDBC应用时,数据库连接管理与Java名字和目录接口(JNDI)是集成在一起的。遍布企业的数据源的属性可以存储在一个目录中,采用这种方式使得我们可以集中管理用户名、密码、数据库名和JDBC URL。

在这样的环境中,可以使用下列代码创建数据库连接:

var jndiContext = new InitialContext();
var source = (DataSource) jndiContext.lookup("java:comp/env/jdbc/corejava");
Connection conn = source.getConnection();

请注意,我们不再使用 DriverManager,而是使用 JNDI 服务来定位数据源。数据源是一个能够提供简单的 JDBC 连接和更多高级服务的接口,比如执行涉及多个数据库的分布式事务。javax.sql 标准扩展包定义了 DataSource 接口。

直 注释: 在 Java EE 的容器中, 甚至不必编程进行 JNDI 查找, 只需在 DataSource 域上使用 Resource 注解, 当加载应用时, 这个数据源引用将被设置:

@Resource(name="jdbc/corejava")
private DataSource source;

当然,我们必须在某个地方配置数据源。如果你编写的数据库程序将在 Servlet 容器中运行,比如 Apache Tomcat,或在应用服务器中运行,比如 GlassFish,那么必须将数据库配置

*信息 包括JNDI名字、JDBC URL. 户名和密 放 在 文件中 或 在 员GUI 中进行设置。*

*户名 和 录 只是众多 别关注 之一。另一个 则涉及建 数据库 接所需的开 。我们 例数据库 序使 了两 来 取数据库 接 序清 单5-3中 QueryDB 序在 序 开头建 了到数据库 单个 接 并在 序 尾处关 了 它 而程序清单5-4中 ViewDB 序在每次 时 会打开一个新 接。*

*但是 两 方式 不令人满意 因为数据库 接是有 源 如果 户 开应 一段时 么他占 接就不应 保持打开 态 另外 每次査 取 接并在 后 关 它 代价也是 当 。*

*决上 方法是建 数据库 接池 pool 。 意味 数据库 接在 上并未 关 是保 在一个 列中并 反复重用。 接池是一 常 服务 JDBC 为 实 提供了 以实 接池服务 手段。不 JDK本 并未实 服务 数据库供应 商提供 JDBC 动 序中 常也不包含这项服务。 反 Web容器和应 服务器 开发商 常会提供 接池服务 实 。*

*接池 使 对 序员来 是完全 明 可以通过获取数据源并调用getConnection 方法来得到 接池中 接。使 完 接后 dose方法。 方法并不会在物理上 关 接 只是告 接池已 使 完 接。 接池 常 会将池机制作 于 备 句上。*

*此 你已 学会了 JDBC 基本知识 并且已 如何实 单 数据库应 。然 正如我们在本 开头所强 样 数据库的相关技术 常复杂 本 属于介 性 当多 已 出了本 围。如果 全 了 JDBC的高级功 参 JDBC API Tutorial and Reference 或 JDBC 。*

*在本 中 我们学习了如何 Java操作关 型数据库。下一 将讨论Java 8 口期和时 库。*

## *6 曰期和时 API*

- *▲<sup>时</sup>*
- *▲本地日期*
- *▲日期 整器*
- *▲本地时*

- *▲时区时*
- *▲格式化和 <sup>析</sup>*
- *▲与遗留代码的互操作*

*光 似 我们可以很容易地 一个 点 然后向前和向后以 来 时。 为什么处 <sup>时</sup> 会显得如此之 <sup>呢</sup> 出在人 <sup>上</sup>。如果我们只 <sup>告</sup> 对方 "1523793600<sup>时</sup> 来 我 别 到 " 么一切 会很 单。但是我们希望时 够和朝夕与季 挂 就使 事情变得复杂了。Java 1.0有一个Date 事后 明它 于 单了 当Java 1.1引人Calendar 之后 Date 中 大 分方法就 弃 了。但是 Calendar API 不够 力 它 实例 是可修改 并且它没有处 如 样 。 3次升 很吸引人 就是Java 8<sup>中</sup> 引人 java.time API,它修正了 去 并且应 会服役 当长的一段时 。在本 中 你将会学习是什么使时 变得如此烦人 以及日期和时 API是如何 决 些问题的。*

## *6.1<sup>时</sup>*

*在历史上 基本 时 单位" "是从地 中推导出来 。地 一周 24 个小时 即24x60x60=86 400 因此 来 好像只是一个有关如何 定义1秒的 天文度 。 憾 是 地 有 微 摄动 所以 更加 定义。1967年 人们根 据 133原子内在 性推导出了与历史定义 匹 新 定义。 以后 一 一个原子 来 护 官方时 。*

*官方时 护器时常 将 对时 与地 同步。 先 官方 作 整 从1972年开始 偶尔需要插人"闰秒"。 在 上 偶尔也 1 但是 从来没发 。 又是有关修改 时 。很明显 是个 点 多计算机 使 "平滑"方式来人为地在 之前 时 变慢或变快 以保 每天 是86 400 。 做法可以奏效 因为 机上 本地时 并 么 机也惯于将 时 与外 时 服务 同步。*

*Java Date和Time API 求Java使 时 尺度为*

- *每天86 400*
- *每天正午与官方时 匹*
- *・在其他时 点上 以 定义 方式与官方时 接 匹*

*予了 Java很大 灵活性 使其可以进行调整 以 应官方时 未来 变化。*

*在Java中 Instant 时 上 某个点。 为"新 元" 时 原点 为 伦 敦格林尼治 家天文台 本初子午 所处时区 <sup>1970</sup>年1月1<sup>日</sup> 午夜。 与UNIX/POSIX<sup>时</sup> 中使 惯例 同。从 原点开始 时 按照每天86400 向前或向回度 精确到纳秒。Instant 值往回可 溯10亿年(Instant.MIN)o 对于 宇宙年 (大 135亿年)来 差得 但是 对于所有实 应 来 应该足够了。毕 10亿年前 地球表面还覆盖着冰层 只有当今植 和 动 微 先在 殖 。最大 值Instant.MAX是公元<sup>1</sup> 000000000年 12月31<sup>日</sup>。*

*态方法 Instant.now()<sup>会</sup> 出当前 时刻。你可以按照常 方式 equals<sup>和</sup> compareTo方法来比 两个Instant对 因此你可以将Instant对 作时 戳。*

*为了得到两个时刻之 时 差 可以使 态方法Du ration. between。例如 下 代 展 了如何度 法 时*

*Instant start <sup>=</sup> Instant.now(); runAlgorithmO; Instant end = Instant.now(); Duration timeElapsed = Duration.between(start, end); long millis <sup>=</sup> timeElapsed.toMiUisO;*

*Duration是两个时刻之 时 。你可以 toNanos、toMiUis、getSeconds. toMinutes. toHours和toDays来 得Duration按照传 单位度 时 度。*

*@ <sup>注</sup> <sup>在</sup>Java8<sup>中</sup> <sup>必</sup> getSeconds 不是toSeconds。*

*如果想 到 么就 当心上溢 。long值可以存储大 300年 时 对应 数。如果你 Duration 于 个时 么可以 接将其 换为 数。你可以使 更长的Duration,即 Duration对象用一个long来存储 数 另外一个 int来存储 <sup>数</sup>。Duration接口包含了大 在本 末尾展 于执 <sup>术</sup> 方法。*

*例如 如果想 检査某个 法是否 少比另4 法快10<sup>倍</sup> 么你可以执 如下的计算:*

*Duration timeElapsed2 <sup>=</sup> Du ration.between(start2, end2); boolean overTenTimesFaster*

*=timeElapsed. multipliedBy (10) .minus(timeEl.apsed2) .isNegativeO;*

*只展 了 法。因为 法不会 数 年 所以可以 接使 下 方法*

*boolean overTenTimesFaster = timeElapsed.toNanosd \* 10 < timeElapsed2.toNanos();*

*<sup>匯</sup> 注 Instant和Duration 是不可修改 所以 如multipliedBy和minus 样 方法 会 回一个新 实例。*

*在 序清单6-1 例 序中 可以 到如何使 Instant和Duration 来对两个 法 时。*

#### *序清单 6-1 timeline/TimeLinejava*

```
1 package timeline;
```

```
* @version 1.01 2021-09-06
    * @author Cay Horstmann
6
8 import java.time.*;
9 import java.util.*;
   import java.util.stream.*;
10
12 public class Timeline
13
      public static void main(String[] args)
14
15
         Instant start = Instant.now();
16
         runAlgorithm();
17
18
         Instant end = Instant.now();
         Duration timeElapsed = Duration.between(start, end);
19
         long millis = timeElapsed.toMillis();
28
         System.out.printf("%d milliseconds\n", millis);
21
22
         Instant start2 = Instant.now();
23
24
         runAlgorithm2();
         Instant end2 = Instant.now();
25
         Duration timeElapsed2 = Duration.between(start2, end2);
26
         System.out.printf("%d milliseconds\n", timeElapsed2.toMillis());
27
          boolean overTenTimesFaster = timeElapsed.multipliedBy(10)
28
             .minus(timeElapsed2).isNegative();
29
         System.out.printf("The first algorithm is %smore than ten times faster",
38
            overTenTimesFaster ? "" : "not ");
31
32
33
      public static void runAlgorithm()
34
35
          int size = 10;
36
          ArrayList<Integer> list = new Random().ints().map(i -> i % 100).limit(size)
37
             .boxed().collect(Collectors.toCollection(ArrayList::new));
38
39
          Collections.sort(list);
          System.out.println(list);
48
41
47
      public static void runAlgorithm2()
43
44
          int size = 10;
45
46
          List<Integer> list = new Random().ints().map(i -> i % 100).limit(size)
             .boxed().collect(Collectors.toCollection(ArrayList::new));
47
          while (!IntStream.range(1, list.size())
AR.
                .allMatch(i -> list.get(i - 1).compareTo(list.get(i)) <= θ))</pre>
49
             Collections.shuffle(list);
          System.out.println(list);
51
52
53 }
```

#### API java.time.Instant

static Instant now()

*从最佳 可 时 中 取当前 时刻。*

- *• Instant plus(TemporalAmount amountToAdd)*
- *• Instant minus(TemporalAmount amountToSubtract) 产 一个时刻 时刻与当前时刻 定 时 。Duration和Period (参 6.2 )实 了 TemporalAmount 接口。*
- *• Instant (plus Iminus)(Nanos IMillis ISeconds)(long number) 产 一个时刻 时刻与当前时刻 定数 、微 或 。*

#### *am| java.time.Duration*

- *• static Duration of(Nanos <sup>I</sup> Millis <sup>I</sup> Seconds <sup>I</sup> Minutes <sup>I</sup> Hours <sup>I</sup> Days)(long number) 产 一个 定数 指定时 单位 时 。*
- *• static Duration between(Temporal startlnclusive, Temporal endExclusive) 产 一个在 定时 点之 Duration对 。Instant 实 了 Temporal接口 LocalDate/LocalDateTime/LocalTime (参 6.4 )和 ZonedDateTime (参 6.5 )也实 了 接口。*
- *• long toNanosO*
- *• long toMillisO*
- *• long toSeconds() <sup>9</sup>*
- *• long toMinutesO*
- *• long toHoursO*
- *• long toSecondsf)*
- *• long toSecondsO*
- *• long toDaysO*

*取当前时 按照方法名中 时 单位度 数 。*

- *• int to(Nanos <sup>I</sup> Millis <sup>I</sup> Seconds <sup>I</sup> Minutes <sup>I</sup> Hours)Part ()*
- *• long to(Days <sup>I</sup> Hours <sup>I</sup> Minutes <sup>I</sup> Seconds <sup>I</sup> Millis <sup>I</sup> Nanos)Part () 当前时 中 定时 单位 分。例如 在100 时 中 分 分是1, 秒的部分是40。*
- *• Instant plus(TemporalAmount amountToAdd)*
- *• Instant minus(TemporalAmount amountToSubtract) 产 一个时刻 时刻与当前时刻 定 时 。Duration和Period (参 6.2 )实 了 TemporalAmount 接口。*
- *• Duration multipliedBydong multiplicand)*
- *• Duration dividedBy(long divisor)*
- *• Duration negated() <sup>产</sup> 一个时 <sup>时</sup> <sup>是</sup> 当前时刻乘以或 <sup>以</sup> <sup>定</sup> <sup>或</sup>-1得到 。*

- *• boolean isZeroO*
- *• boolean isNegativeO 如果当前Duration对 是0或 数 则 回true。*
- *• Duration (plus <sup>I</sup> minus)(Nanos <sup>I</sup> Millis <sup>I</sup> Seconds <sup>I</sup> Minutes <sup>I</sup> Hours <sup>I</sup> Days)(long number) 产 一个时 时 是 当前时刻加上或减去 定 数最 指定时 单位 得到 。*

## *6.2本地曰期*

*在 我们从 对时 向人 时 。在Java API中有两 人 时 本地日期/ 时 和时区时 。本地日期/时 包含日期和当天 时 但是与时区信息没有任何关 。 <sup>1903</sup>年6月<sup>14</sup> H就是一个本地日期 例(lambda演 发明 Alonzo Church<sup>在</sup> 一天 诞生)。因为 个日期既没有当天 时 也没有时区信息 因此它并不对应 时刻。与 之 反 是 <sup>1969</sup>年7月16日09:32:00 EDT ( 波 11号发射 时刻)是一个时区日期/ 时 表示的是时间线上 一个精确的时刻。*

*有 多 并不 时区 在某些情况下 时区 是一 。假 你安排每周 10:00开一次会。如果你加7天(即<sup>7</sup> <sup>x</sup> <sup>24</sup> x <sup>60</sup> x 60 )到最后一次会 时区时 上 <sup>么</sup> 你可 会 巧 了夏令时 时 整 次会 可 会早一小时或晚一小时*

*正是 到 个原因 API的设计者们推荐程序员不 使 时区时 实想 对时 实例。 日、假日、 划时间等通常最好都表示成本地日期和时 。*

*LocalDate是带有年、月、日 日期。为了构建LocalDateX<sup>寸</sup> 可以使 now或of 态方法*

```
LocalDate today = LocalDate.now(); // Today's date
LocalDate alonzosBirthday = LocalDate.of(1903, 6, 14);
alonzosBirthday = LocalDate.of(1903, Month.JUNE, 14);
   // Uses the Month enumeration
```

*与UNIX和java.util.Date中使 月从0开始 年从1900开始计算的不 则 惯 法不同 你 提供 常使 月份 数字。或 你可以使 Month枚举。*

*本 末尾展 丫最有用的操作LocalDate对象的方法。*

*例如 序员日是每年 256天。下 展 了如何很容易地计算出它*

```
LocalDate programmersDay = LocalDate.of(2014, 1, l).plusDays(255);
   // September 13r but in a leap year it would be September 12
```

*回忆一下 两个Instant之 时 是Duration, 于本地日期 价 是Period, 它 是流 年、月或日 数 。可以 birthday.plus(Period.ofYears(l))来 取下 一年的生日。当然 也可以 接 birthday.plusYears(l)<sup>o</sup> 但是 birthday.plus(Duration. ofDays(365))在 年是不会产 正 果 。*

*util方法会产 两个本地日期之 <sup>时</sup> 。例如*

*independenceDay.until(Christmas)*

*会产 5个月21天 一段时 。 实 上并不是很有 因为每个月 天数不尽 同。<sup>为</sup>*

*了 定到底有多少天 可以使*

*ind即endenceDay.until(Christmas, ChronoUnit.DAYS) // <sup>174</sup> days*

*令 告 LocalDate API中 有些方法可 会创建出并不存在 日期。例如 在1月<sup>31</sup> 日上加上1个月不应 <sup>产</sup> 2月31日。 些方法并不会抛出异常 是会 <sup>回</sup> <sup>月</sup> 有效 最后一天。例如*

*LocalDate.of(2016, 1, 31).plusMonths(l)*

*和*

*LocalDate.of(2816, 3, 31).minusMonths(l)*

*将产 <sup>2016</sup>年2月29<sup>曰</sup>。*

*getDayOfWeek会产 星期日期 即DayOfWeek枚举 某个值。DayOfWeek.MONDAY 枚举值 为1 DayOfWeek.SUNDAY 枚举值为7。例如*

*LocalDate.of(1900, 1, 1).getDayOfWeek().getValue()*

*会产 <sup>1</sup>。DayOfWeek枚举具有便捷方法plus和minus,以7为模 星期日期。例如,DayOf-Week. SATURDAY, plus (3) 会产 DayOfWeek.TUESDAY□*

*0 <sup>注</sup> 周末实 上在每周 末尾。 <sup>与</sup>java.util.Calendar有所差异 在后 <sup>中</sup> <sup>星</sup> 期日 值为1, 星期六 值为7。*

*Java 9添加了两个有 datesUntil方法 它们会产 LocalDate对 流。*

```
LocalDate start = LocalDate.of(2000, 1, 1);
LocalDate endExclusive = LocalDate.nowf);
Stream<LocalDate> allDays = start.datesUntil(endExclusive);
Stream<LocalDate> firstDaysInMonth = start.datesUntil(endExclusive, Period.ofMonths(l));
```

*了 LocalDate之外 有MonthDay、YearMonth和Yea「 可以描 分日期。例如 <sup>12</sup> 月25日(没有指定年份)可以 成一个MonthDay对 。*

*序清单6-2中 例 序展 了如何使 LocalDate 。*

#### *序清单 6-2 localdates/LocalDates.令java ' ' <sup>T</sup> <sup>I</sup> <sup>J</sup> <sup>v</sup> v"-\* <sup>u</sup> <sup>I</sup> <sup>I</sup> -*

```
1 package localdates;
2
3 /*»
4 * ©version 1.61 2921-99-96
5 * ^author Cay Horstmann
6 /
7 import java.time.*;
8 import java.time.temporal.*;
9 import java.util.stream.*;
le
n public class LocalDates
13 public static void main(String[] args)
```

```
14
         LocalDate today = LocalDate.now(); // Today's date
15
         System.out.println("today: " + today);
16
17
         LocalDate alonzosBirthday = LocalDate.of(1903, 6, 14);
18
         alonzosBirthday = LocalDate.of(1903, Month.JUNE, 14);
19
         // Uses the Month enumeration
28
         System.out.println("alonzosBirthday: " + alonzosBirthday);
21
22
         LocalDate programmersDay = LocalDate.of(2018, 1, 1).plusDays(255);
23
         // September 13, but in a leap year it would be September 12
24
         System.out.println("programmersDay: " + programmersDay);
25
26
         LocalDate independenceDay = LocalDate.of(2018, Month.JULY, 4);
27
         LocalDate christmas = LocalDate.of(2018, Month.DECEMBER, 25);
28
29
         System.out.println("Until christmas: " + independenceDay.until(christmas));
30
         System.out.println("Until christmas: "
31
            + independenceDay.until(christmas, ChronoUnit.DAYS));
32
33
         System.out.println(LocalDate.of(2016, 1, 31).plusMonths(1));
34
         System.out.println(LocalDate.of(2016, 3, 31).minusMonths(1));
35
36
         DayOfWeek startOfLastMillennium = LocalDate.of(1900, 1, 1).getDayOfWeek();
37
         System.out.println("startOfLastMillennium: " + startOfLastMillennium);
38
         System.out.println(startOfLastMillennium.getValue());
         System.out.println(DayOfWeek.SATURDAY.plus(3));
48
41
         LocalDate start = LocalDate.of(2000, 1, 1);
42
         LocalDate endExclusive = LocalDate.now();
43
         Stream<LocalDate> firstDaysInMonth = start.datesUntil(endExclusive, Period.ofMonths(1));
44
         System.out.println("firstDaysInMonth: "
45
            + firstDaysInMonth.toList());
46
47
   }
48
```

#### API java.time.LocalDate

- static LocalDate now()
   获取当前的 LocalDate。
- static LocalDate of(int year, int month, int dayOfMonth)
- static LocalDate of (int year, Month month, int dayOfMonth)
   用给定的年、月(1到12之间的整数或者 Month 枚举的值)和日(1到31之间)产生 一个本地日期。
- LocalDate (plus | minus)(Days | Weeks | Months | Years)(long number)
   产生一个 LocalDate,该对象是通过在当前对象上加上或减去给定数量的时间单位获得的。
- LocalDate plus(TemporalAmount amountToAdd)
- LocalDate minus(TemporalAmount amountToSubtract)
   产生一个时刻,该时刻与当前时刻距离给定的时间量。Duration 和 Period 类实现了

*Tempo ralAmount 接口。*

- *• LocalDate withDayOfMonth(int dayOfMonth)*
- *• LocalDate withDayOfYear(int dayOfYear)*
- *• LocalDate withMonth(int month)*
- *• LocalDate withYear(int year) 回一个新 LocalDate,将月份日期、年日期、月或年修改为 定值。*
- *<sup>參</sup> int getDayOfMonthO 取月份日期(1到31<sup>之</sup> )。*
- *• int getDayOfYear() 取年日期(1到366之 )。*
- *• DayOfWeek getDayOfWeek() 取星期日期 回某个DayOfWeek枚举值。*
- *• Month getMonth()*
- *<sup>參</sup> int getMonthValueO 取 Month枚举值 月份 或者用1到12之间的数字表示的月份。*
- *• int getYear() 取年份 在-999 <sup>999</sup> 999到<sup>999</sup> <sup>999</sup> 999之 。*
- *• Period until(ChronoLocalDate endDateExclusive) 取 到 定 止日期 periodo LocalDate和date 对 公历实 了 ChronoLocalDate 接口。*
- *• boolean isBefore(ChronoLocalDate other)*
- *• boolean isAfter(ChronoLocalDate other) 如果 日期在 定日期之前或之后 则 回true。*
- *• boolean isLeapYearO*

*如果当前是 年 则 回true。BP, 年份 够 4整 但是不能被100整 <sup>或</sup> 者能够 400整 。 法应 可以应 于所有已 去 年份 尽 在历史上它并 不准 ( 年是在公元前46年发明出来 涉及整 100和400的规则是在<sup>1582</sup> 年 公历改 中引人 。 场改 历了 300年才 广泛接受)。*

- *• Stream<LocalDate> datesUntil(LocalDate endExclusive)*
- *• Stream<LocalDate> datesUntil(LocalDate endExclusive, Period step) 产 一个日期流 从当前 LocalDate对 参数endExclusive指定 日期 其中 <sup>步</sup> 尺寸为1,<sup>或</sup> <sup>是</sup> <sup>定</sup> period。*

#### *java.ti .Period*

- *• static Period of(int years, int months, int days)*
- *• Period of(Days <sup>I</sup> Weeks <sup>I</sup> Months <sup>I</sup> Years) (int number)*

*定数 时 单位产 一个Period对 。*

- *• int get(Days| Months <sup>I</sup> Years)() 取当前Period对象的日、月或年。*
- *• Period (plus Iminus)(DaysI Months IYears)(long number) 产 一个LocalDate, 对 是 在当前对 上加上或减去 定数 时 单位 得 。*
- *<sup>參</sup> Period plus(TemporalAmount amountToAdd)*
- *• Period minus(TemporalAmount amountToSubtract) 产 一个时刻 时刻与当前时刻 定 时 。Duration和Period 实 了 Tempo ralAmount 接口。*
- *• Period with(Days <sup>I</sup> Months <sup>I</sup> Years)(int number) 回一个新 Period,将日、月、年修改为 定值。*

## *6.3曰期 整器*

*对于日 安排应 来 常 如"每个月的第一个星期二" 样 日期。 TemporalAdjusters 提供了大 于常 整 态方法。你可以将 整方法 果传 with方法。例如 某个月 一个星期二可以像下 样*

```
LocalDate firstTuesday = LocalDate.of(year, month, l).with(
  Tempo ralAdj usters.nextOrSame(DayOfWeek.TUESDAY));
```

*一如既往 with方法会 回一个新 LocalDate对 不会修改原来 对 。本 末 尾展 了有关可 整器 API 明。*

*可以 实 TemporalAdjuster接口来创建 己 整器。下 是 于计算下一个工 作日 整器。*

```
TemporalAdjuster NEXT_WORKDAY = w ->
   {
      var result = (LocalDate) w;
      do
      {
         result = result.plusDays(l);
      }
      while (result.getDayOfWeek(),getValue() >= 6);
      return result;
   }
```

*LocalDate backToWork <sup>=</sup> today.with(NEXT WORKDAY);*

*注意 lambda 式 参数 型为Temporal,它必 强制 型为LocalDate。你可以 ofDateAdjuster方法来 免 强制 型 方法期望得到 参数是 型为UnaryOperator <LocalDate> lambda 式。*

```
TemporalAdjuster NEXTWORKDAY = Tempo ralAdj uste rs. ofDateAdj uster (w ->
   {
      LocalDate result = w; // No cast
```

```
result = result.plusDays(l);
   }
   while (result.getDayOfWeek().getValue() >= 6);
   return result;
})
```

#### *"| java.tifie.LocaWate*

*• LocalDate with(TemporalAdjuster adjuster) 回 日期 定 整器 整后 果。*

#### *ah<sup>|</sup> java.tine.temporal.TemporalAdjusters*

- *• static TemporalAdjuster next(DayOfWeek dayOfWeek)*
- *• static TemporalAdjuster nextOrSame(DayOfWeek dayOfWeek)*
- *• static TemporalAdjuster previous(DayOfWeek dayOfWeek)*
- *• static TemporalAdjuster previousOrSame(DayOfWeek dayOfWeek) 回一个 整器 于将日期 整为 定 星期日期。*
- *• static TemporalAdjuster dayOfWeeklnMonthfint n, DayOfWeek dayOfWeek)*
- *• static TemporalAdjuster lastInMonth(DayOfWeek dayOfWeek) 回一个 整器 于将日期 整为月份中 n个或最后一个 定 星期日期。*
- *• static TemporalAdjuster firstDayOfMonthO*
- *• static TemporalAdjuster firstDayOfNextMonthf)*
- *• static TemporalAdjuster firstDayOfYear()*
- *• static TemporalAdjuster firstDayOfNextYearO*
- *• static TemporalAdjuster lastDayOfMonthO*
- *• static TemporalAdjuster lastDayOfYear() 回一个 整器 于将日期 整为月份或年份中 定 日期。*

## *6.4本地时*

*LocalTime 当日时刻 例如1530:00。可以 now或of方法创建其实例*

```
LocalTime rightNow = LocalTime.now();
LocalTime bedtime = LocalTime.of(22, 30); // or LocalTime.of(22, 30, )
```

*API 明展 了常 对本地时 操作。plus和minus操作是按照一天24小时循 操 作 。例如*

*LocalTime wake<sup>叩</sup>=bedtime.plusHours(8); // wakeup is 6:30:00*

*El<sup>注</sup> LocalTime 并不关心AM/PM。 <sup>愚</sup> <sup>将</sup> <sup>抛</sup> 格式器去 <sup>决</sup> 参 6.6 。*

*有一个 日期和时 LocalDateTime 。 个类适合存储固定时区 时 点 例 如 于排 或排 。但是 如果你 夏令时 或 处 不同时区 户 么就应 使 接下来 ZonedDateTime 。*

#### *awj java.tine.LocalTime*

- *• static LocalTime now() 取当前 LocalTime。*
- *• static LocalTime of(int hour, int minute)*
- *• static LocalTime of(int hour, int minute, int second)*
- *• static LocalTime of(int hour, int minute, int second, int nanoOfSecond) 产 一个LocalTime,它具有 定 小时(0到23之 )、分 、 (0到59之 )和 纳秒(0到<sup>999</sup> <sup>999</sup> 999之 )。*
- *• LocalTime (plus Iminus)(HoursI Minutes <sup>I</sup> Seconds <sup>I</sup> Nanos)(long number) 产 一个LocalTime, 对 是 在当前对 上加上或减去 定数 时 单位 得 。*
- *• LocalTime plus(Tempora1.Amount amountToAdd)*
- *• LocalTime minus(TemporalAmount amountToSubtract) 产 一个时刻 时刻与当前时刻 定 时 。*
- *• LocalTime with(Hour <sup>I</sup> Minute <sup>I</sup> Second <sup>I</sup> Nano)(int value) 回一个新 LocalTime,将小时、分 、 或纳秒修改为 定值。*
- *• int getHourO 取小时(0到23之 )。*
- *• int getMinute()*
- *• int getSecond() 取分 或 (0到59之 )。*
- *• int getNanof) 取纳秒(0到<sup>999</sup> <sup>999</sup> 999之 )。*
- *• int toSecondOfDayO*
- *• long toNanoOfDayO 产 午夜到当前LocalTime 或 数。*
- *• boolean isBefore(LocalTime other)*
- *• boolean isAfter(LocalTime other) 如果当期日期在 定日期之前或之后 则 冋true。*

## *6.5时区时*

*时区可 比地 不 则 旋 方式引 复杂性 烦 因为它完全是人 出来*

概念。在理性的世界中,我们都会遵循格林尼治时间,有些人在02:00 吃午饭,而有些人却在22:00 吃午饭。中国横跨了4个时区,但是使用了同一个时间。在其他地方,时区划分显得并不规则,并且还有国际日期变更线,而夏令时则使事情变得更复杂了。

尽管时区显得变化繁多,但这就是无法回避的现实生活。在实现日历应用时,它需要能够为坐飞机在不同国家之间穿梭的人们提供服务。如果你有个 10:00 在纽约召开的电话会议,但是碰巧你人在柏林,那么你肯定希望该应用能够在正确的本地时间点上发出提醒。

互联网编码分配管理机构(Internet Assigned Numbers Authority, IANA)保存着一个数据库,里面存储着世界上所有已知的时区(www.iana.org/time-zones),它每年会更新数次,其中许多更新是为了处理夏令时的变更规则。Java 使用了 IANA 数据库。

每个时区都有一个 ID, 例如 America/New\_York 和 Europe/Berlin。要想找出所有可用的时区,可以调用 ZoneId.getAvailableZoneIds。在本书撰写之时,有将近 600 个 ID。

给定一个时区 ID, 静态方法 ZoneId.of(id) 可以产生一个 ZoneId 对象。可以通过调用 local.at-Zone(zoneId) 用这个 ZoneID 对象将 LocalDateTime 对象转换为 ZonedDateTime 对象,或者可以通过调用静态方法 ZonedDateTime.of(year,month,day,hour,minute,second,nano,zoneId) 来构造一个 Zoned-DateTime 对象。例如,

```
ZonedDateTime apollo11launch = ZonedDateTime.of(1969, 7, 16, 9, 32, 0, 0,
    ZoneId.of("America/New_York"));
    // 1969-07-16T09:32-04:00[America/New_York]
```

这是一个具体的时刻,调用 apollo11launch.toInstant 可以获得对应的 Instant 对象。反过来,如果你有一个时刻对象,调用 instant.atZone(ZoneId.of("UTC")) 可以获得格林尼治皇家天文台的 ZonedDateTime 对象,或者使用其他的 ZoneId 获得地球上其他地方的 ZoneId。

注释: UTC代表"协调世界时",这是英文"Coordinated Universal Time"和法文 "Temps Universel Coordiné"首字母缩写的折中,它与这两种语言中的缩写都不一致。 UTC是不考虑夏令时的格林尼治皇家天文台时间。

ZonedDateTime 的许多方法都与 LocalDateTime 的方法相同(参见本节末尾的 API 说明),它们大多数都很直观,但是夏令时带来了一些复杂性。

当夏令时开始时,时钟要向前拨快一小时。当你构建的时间对象正好落入了这跳过去的一个小时内时,会发生什么?例如,在 2013 年,中欧地区在 3 月 31 日 2:00 切换到夏令时,如果你试图构建的时间是不存在的 3 月 31 日 2:30,那么你实际上得到的是 3:30。

```
ZonedDateTime skipped = ZonedDateTime.of(
  LocalDate.of(2013, 3, 31),
  LocalTime.of(2, 30),
  ZoneId.of("Europe/Berlin"));
  // Constructs March 31 3:30
```

反过来,当夏令时结束时,时钟要向回拨慢一小时,这样同一个本地时间就会出现两次。当你构建位于这个时间段内的时间对象时,就会得到这两个时刻中较早的一个:

```
ZonedDateTime ambiguous = ZonedDateTime.of(
  LocalDate.of(2013, 10, 27), // End of daylight savings time
  LocalTime.of(2, 30),
  ZoneId.of("Europe/Berlin"));
  // 2013-10-27T02:30+02:00[Europe/Berlin]
ZonedDateTime anHourLater = ambiguous.plusHours(1);
  // 2013-10-27T02:30+01:00[Europe/Berlin]
```

一个小时后的时间会具有相同的小时和分钟, 但是时区的偏移量会发生变化。

你还需要在调整跨越夏令时边界的日期时特别注意。例如,如果你将会议设置在下个星期,不要直接加上一个7天的 Duration:

```
ZonedDateTime nextMeeting = meeting.plus(Duration.ofDays(7));
// Caution! Won't work with daylight savings time
```

而是应该使用 Period 类。

ZonedDateTime nextMeeting = meeting.plus(Period.ofDays(7)); // OK

● 警告: 还有一个 OffsetDateTime 类,它表示与 UTC 具有偏移量的时间,但是没有时区规则的束缚。这个类被设计用于专用应用,这些应用特别需要剔除这些规则的约束,例如某些网络协议。对于人类时间,还是应该使用 ZonedDateTime。

程序清单 6-3 中的示例程序演示了 ZonedDateTime 类的用法。

#### 程序清单 6-3 zonedtimes/ZonedTimes.java

```
package zonedtimes;
2
3 /**
4 * @version 1.0 2016-05-10
* @author Cay Horstmann
6 */
8 import java.time.*;
10 public class ZonedTimes
11 {
      public static void main(String[] args)
12
13
         ZonedDateTime apollo11launch = ZonedDateTime.of(1969, 7, 16, 9, 32, 0, 0,
14
            ZoneId.of("America/New York")); // 1969-07-16T09:32-04:00[America/New York]
15
         System.out.println("apollo11launch: " + apollo11launch);
16
17
         Instant instant = apollolllaunch.toInstant();
18
         System.out.println("instant: " + instant);
19
20
         ZonedDateTime zonedDateTime = instant.atZone(ZoneId.of("UTC"));
21
         System.out.println("zonedDateTime: " + zonedDateTime);
22
         ZonedDateTime skipped = ZonedDateTime.of(LocalDate.of(2013, 3, 31),
24
            LocalTime.of(2, 30), ZoneId.of("Europe/Berlin")); // Constructs March 31 3:30
25
         System.out.println("skipped: " + skipped);
```

```
27
         ZonedDateTime ambiguous = ZonedDateTime.of(
28
            LocalDate.of(2013, 10, 27), // End of daylight savings time
29
            LocalTime.of(2, 30), ZoneId.of("Europe/Berlin"));
38
            // 2013-10-27T02:30+02:00[Europe/Berlin]
31
         ZonedDateTime anHourLater = ambiguous.plusHours(1);
37
            // 2013-10-27T02:30+01:00[Europe/Berlin]
33
         System.out.println("ambiguous: " + ambiguous);
34
         System.out.println("anHourLater: " + anHourLater);
35
36
         ZonedDateTime meeting = ZonedDateTime.of(LocalDate.of(2013, 10, 31),
37
            LocalTime.of(14, 30), ZoneId.of("America/Los Angeles"));
38
         System.out.println("meeting: " + meeting);
39
         ZonedDateTime nextMeeting = meeting.plus(Duration.ofDays(7));
48
            // Caution! Won't work with daylight savings time
41
         System.out.println("nextMeeting: " + nextMeeting);
42
         nextMeeting = meeting.plus(Period.ofDays(7)); // OK
43
44
         System.out.println("nextMeeting: " + nextMeeting);
      }
45
45 }
```

#### API java.time.ZonedDateTime

- static ZonedDateTime now()
   获取当前的 ZonedDateTime。
- static ZonedDateTime of(int year, int month, int dayOfMonth, int hour, int minute, int second, int nanoOfSecond, ZoneId zone)
- static ZonedDateTime of(LocalDate date, LocalTime time, ZoneId zone)
- static ZonedDateTime of(LocalDateTime localDateTime, ZoneId zone)
- static ZonedDateTime ofInstant(Instant instant, ZoneId zone)
  用给定的参数和时区产生一个 ZonedDateTime。
- ZonedDateTime (plus | minus)(Days | Weeks | Months | Years | Hours | Minutes | Seconds | Nanos)(long number)

产生一个 ZonedDateTime, 该对象是通过在当前对象上加上或减去给定数量的时间单位获得的。

- ZonedDateTime plus(TemporalAmount amountToAdd)
- ZonedDateTime minus(TemporalAmount amountToSubtract)
   产生一个时刻,该时刻与当前时刻相差给定的时间量。
- ZonedDateTime with(DayOfMonth|DayOfYear|Month|Year|Hour|Minute|Second|Nano)(int value) 返回一个新的 ZonedDateTime, 用给定的值替换给定的时间单位。
- ZonedDateTime withZoneSameInstant(ZoneId zone)
- ZonedDateTime withZoneSameLocal(ZoneId zone)
   返回一个新的 ZonedDateTime, 位于给定的时区,它与当前对象要么表示相同的时刻,要么表示相同的本地时间。

- *• int getDayOfMonth() 取月份日期(1到31之 )。*
- *• int getDayOfYearO 取年份日期(1到366之 )。*
- *• DayOfWeek getDayOfWeek() 取星期日期 回DayOfWeek枚举 值。*
- *• Month getMonth()*
- *• int getMonthValueO 取 Month枚举值 月份 或 1到12之间的数字表示的月份。*
- *• int getYear() 取年份 在-999 <sup>999</sup> 999到<sup>999</sup> <sup>999</sup> 999之 。*
- *• int getHour() 取小时(0到23之 )。*
- *• int getMinuteO*
- *• int getSecondO 取分 到 (0到59之 )。*
- *• int getNanoO 取纳秒(0到<sup>999</sup> <sup>999</sup> 999之 )。*
- *• public ZoneOffset getOffsetO 取与UTC <sup>时</sup> <sup>差</sup> 。<sup>差</sup> 可在-12:00〜4-14:00变化。有些时区 有小数时 差。时 差会 夏令时变化。*
- *• LocalDate toLocalDate()*
- *• LocalTime toLocalTimeO*
- *• LocalDateTime toLocalDateTimeO*
- *• Instant tolnstant() 成当地日期、时 或日期/时 或 应 。*
- *• boolean isBefore(ChronoZonedDateTime other)*
- *• boolean isAfter(ChronoZonedDateTime other) 如果 个时区日期/时 在 定 时区日期/时 之前或之后 则 回true。*

## *6.6格式化和 <sup>析</sup>*

*DateTimeFormatter 提供了三 于打印日期/时 值 格式器:*

- *定义 格式器(参 6-1)*
- *• locale 关 格式器*
- *带有定制模式 格式器*

| 格式器                                                        | 描述                                                                       | 示 例                                                                                  |
|------------------------------------------------------------|--------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| BASIC_ISO_DATE                                             | 年、月、日、时区偏移量,中间没有分隔符                                                      | 19690716-0500                                                                        |
| ISO_LOCAL_DATE, ISO_LOCAL_TIME, ISO_LOCAL_DATE_TIME        | 分隔符为 - 、: 、□                                                             | 1969-07-16, 09:32:00,<br>1969-07-16T09:32:00                                         |
| ISO_OFFSET_DATE, ISO_OFFSET_<br>TIME, ISO_OFFSET_DATE_TIME | 类似 ISO_LOCAL_XXX,但是有时区偏移量                                                | 1969-07-16-05:00, 09:32:00-05:00, 1969-07-<br>16T09:32:00-05:00                      |
| ISO_ZONED_DATE_TIME                                        | 有时区偏移量和时区 ID                                                             | 1969-07-16T09:32:00-05:00[America/New_<br>York]                                      |
| ISO_INSTANT                                                | 在UTC中,用Z时区ID来表示                                                          | 1969-07-16T14:32:00Z                                                                 |
| ISO_DATE, ISO_TIME, ISO_<br>DATE_TIME                      | 类似 ISO_OFFSET_DATE、ISO_OFFSET_TIME 和 ISO_ZONED_<br>DATE_TIME, 但是时区信息是可选的 | 1969-07-16-05:00, 09:32:00-05:00,<br>1969-07-16T09:32:00-05:00[America/New_<br>York] |
| ISO_ORDINAL_DATE                                           | LocalDate 的年和年日期                                                         | 1969-197                                                                             |
| ISO_WEEK_DATE                                              | LocalDate 的年、星期和星期日期                                                     | 1969-W29-3                                                                           |
| RFC_1123_DATE_TIME                                         | 用于邮件时间戳的标准,编纂于RFC822,<br>并在RFC1123 中将年份更新到 4 位                           | Wed, 16 Jul 1969 09:32:00 -0500                                                      |

表 6-1 预定义的格式器

要使用标准的格式器,可以直接调用其 format 方法:

String formatted = DateTimeFormatter.ISO\_OFFSET\_DATE\_TIME.format(apollo11launch);
// 1969-07-16T09:32:00-04:00"

标准格式器主要是为了机器可读的时间戳而设计的。为了向人类读者表示日期和时间,可以使用 locale 相关的格式器。对于日期和时间而言,有 4 种与 locale 相关的格式化风格,即 SHORT、MEDIUM、LONG 和 FULL,参见表 6-2。

| 日 期                      | 时 间                                      |
|--------------------------|------------------------------------------|
| 7/16/69                  | 9:32 AM                                  |
| Jul 16, 1969             | 9:32:00 AM                               |
| July 16, 1969            | 9:32:00 AM EDT                           |
| Wednesday, July 16, 1969 | 9:32:00 AM EDT                           |
|                          | 7/16/69<br>Jul 16, 1969<br>July 16, 1969 |

表 6-2 locale 相关的格式化风格

静态方法 of Localized Date、of Localized Time 和 of Localized Date Time 可以创建这种格式器。例如:

DateTimeFormatter formatter = DateTimeFormatter.ofLocalizedDateTime(FormatStyle.LONG);
String formatted = formatter.format(apollol1launch);
// July 16, 1969 9:32:00 AM EDT

这些方法使用了默认的 locale。为了切换到不同的 locale,可以直接使用 withLocale 方法。

formatted = formatter.withLocale(Locale.FRENCH).format(apollo11launch);
// 16 juillet 1969 09:32:00 EDT

DayOfWeek 和 Month 枚举都有 getDisplayName 方法,可以按照不同的 locale 和格式给出星期日期和月份的名字。

for (DayOfWeek w : DayOfWeek.values())
 System.out.print(w.getDisplayName(TextStyle.SHORT, Locale.ENGLISH) + " ");
 // Prints Mon Tue Wed Thu Fri Sat Sun

请查看第7章以了解更多有关 locale 的信息。

**注释:** java.time.format.DateTimeFormatter 类被设计用来替代 java.util.DateFormat。如果你为了向后兼容性而需要后者的实例,那么可以调用 formatter.toFormat()。

最后,可以通过指定模式来定制自己的日期格式。例如,

formatter = DateTimeFormatter.ofPattern("E yyyy-MM-dd HH:mm");

会将日期格式化为 Wed 1969-07-16 09:32 的形式。按照人们日积月累而制定的显得有些晦涩的规则,每个字母都表示一个不同的时间域,而字母重复的次数对应于所选择的特定格式。表 6-3 展示了最有用的模式元素。

| 时间域或目的              | 示 例                                                         |
|---------------------|-------------------------------------------------------------|
| ERA                 | G: AD, GGGG: Anno Domini, GGGGG: A                          |
| YEAR_OF_ERA         | уу: 69, уууу: 1969                                          |
| MONTH_OF_YEAR       | M: 7, MM: 07, MMM: Jul, MMMM: July, MMMMM: J                |
| DAY_OF_MONTH        | d: 6, dd: 06                                                |
| DAY_OF_WEEK         | e: 3, E: Wed, EEEE: Wednesday, EEEEE: W                     |
| HOUR_OF_DAY         | H: 9, HH: 09                                                |
| CLOCK_HOUR_OF_AM_PM | K: 9, KK: 09                                                |
| AMPM_OF_DAY         | a: AM                                                       |
| MINUTE_OF_HOUR      | mm: 02                                                      |
| SECOND_OF_MINUTE    | ss: 00                                                      |
| NANO_OF_SECOND      | nnnnn: 000000                                               |
| 时区 ID               | VV: America/New_York                                        |
| 时区名                 | z: EDT, zzzz: Eastern Daylight Time V:ET, VVVV:Eastern time |
| 时区偏移量               | x: -04, xx: -0400, xxx: -04:00, XXX: 与 xxx 相同, 但是 Z 表示 0    |
| 本地化的时区偏移量           | 0: GMT-4, 0000: GMT-04:00                                   |
| 修改后的儒略日             | g:58243                                                     |

表 6-3 常用的日期/时间格式的格式化符号

为了解析字符串中的日期/时间值,可以使用众多的静态 parse 方法之一。例如,

LocalDate churchsBirthday = LocalDate.parse("1903-06-14");
ZonedDateTime apollo11launch =

ZonedDateTime.parse("1969-07-16 03:32:00-0400",

DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ssxx"));

第一个调用使用了标准的 ISO\_LOCAL\_DATE 格式器, 而第二个调用使用的是一个定制的格式器。

程序清单6-4中的程序展示了如何格式化和解析日期与时间。

#### 程序清单 6-4 formatting/Formatting.java

```
package formatting;
2
3
    * @version 1.0 2016-05-10
    * @author Cay Horstmann
  import java.time.*;
9 import java.time.format.*;
10 import java.util.*;
   public class Formatting
12
13
      public static void main(String[] args)
14
15
         ZonedDateTime apollo11launch = ZonedDateTime.of(1969, 7, 16, 9, 32, 0, 0,
16
            ZoneId.of("America/New York"));
17
18
         String formatted = DateTimeFormatter.ISO OFFSET DATE TIME.format(apollo11launch);
19
         // 1969-07-16T09:32:00-04:00
20
         System.out.println(formatted);
21
22
         DateTimeFormatter formatter = DateTimeFormatter.ofLocalizedDateTime(FormatStyle.LONG);
23
         formatted = formatter.format(apollo11launch);
24
         // July 16, 1969 9:32:00 AM EDT
25
         System.out.println(formatted);
26
         formatted = formatter.withLocale(Locale.FRENCH).format(apollo11launch);
27
         // 16 juillet 1969 09:32:00 EDT
28
         System.out.println(formatted);
29
38
         formatter = DateTimeFormatter.ofPattern("E yyyy-MM-dd HH:mm");
31
         formatted = formatter.format(apollo11launch);
32
         System.out.println(formatted);
33
34
         LocalDate churchsBirthday = LocalDate.parse("1903-06-14");
35
         System.out.println("churchsBirthday: " + churchsBirthday);
36
         apollo11launch = ZonedDateTime.parse("1969-07-16 03:32:00-0400",
37
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ssxx"));
38
39
         System.out.println("apollo11launch: " + apollo11launch);
49
          for (DayOfWeek w : DayOfWeek.values())
41
            System.out.print(w.getDisplayName(TextStyle.SHORT, Locale.ENGLISH) + " ");
42
43
44 }
```

#### API java.time.format.DateTimeFormatter 🙈

String format(TemporalAccessor temporal)
 格式化给定值。Instant、LocalDate、LocalTime、LocalDateTime 和 ZonedDateTime,以

及许多其他类,都实现了 Temporal Accessor 接口。

- static DateTimeFormatter ofLocalizedDate(FormatStyle dateStyle)
- static DateTimeFormatter ofLocalizedTime(FormatStyle timeStyle)
- static DateTimeFormatter ofLocalizedDateTime(FormatStyle dateTimeStyle)
- static DateTimeFormatter ofLocalizedDateTime(FormatStyle dateStyle, FormatStyle timeStyle) 产生一个用于给定风格的格式器。FormatStyle 枚举的值包括 SHORT、MEDIUM、LONG 和 FULL。
- DateTimeFormatter withLocale(Locale locale)
   用给定的 locale 产生一个等价于当前格式器的格式器。
- static DateTimeFormatter ofPattern(String pattern)
- static DateTimeFormatter ofPattern(String pattern, Locale locale)
   用给定的模式和 locale 产生一个格式器。参阅表 6-3 有关模式的语法。

#### API java.time.LocalDate

- static LocalDate parse(CharSequence text)
- static LocalDate parse(CharSequence text, DateTimeFormatter formatter) 用默认的格式器或给定的格式器产生一个 LocalDate。

#### API java.time.ZonedDateTime

- static ZonedDateTime parse(CharSequence text)
- static ZonedDateTime parse(CharSequence text, DateTimeFormatter formatter) 用默认的格式器或给定的格式器产生一个 ZonedDateTime。

#### 6.7 与遗留代码的互操作

作为全新的创造, Java Date 和 Time API 必须能够与已有类之间进行互操作,特别是无处不在的 java.util.Date、java.util.GregorianCalendar 和 java.sql.Date/Time/Timestamp。

Instant 类近似于 java.util.Date。在 Java 8 中,这个类有两个额外的方法:将 Date 转换为 Instant 的 toInstant 方法,以及反方向转换的静态的 from 方法。

类似地, ZonedDateTime 近似于 java.util.GregorianCalendar, 在 Java 8 中,这个类有细粒度的转换方法。toZonedDateTime 方法可以将 GregorianCalendar 转换为 ZonedDateTime,而静态的 from 方法可以执行反方向的转换。

另一个可用于日期和时间类的转换集位于 java.sql 包中。你还可以传递一个 DateTimeFormatter 给使用 java.text.Format 的遗留代码。表 6-4 对这些转换进行了总结。

表 6-4 java.time 类与遗留类之间的转换

| 类                       | 转换到遗留类             | 转换自遗留类           |
|-------------------------|--------------------|------------------|
| stant<br>java.util.Date | Date.from(instant) | date.toInstant() |

|                                                 | 换到                                          | 换                           |
|-------------------------------------------------|---------------------------------------------|-----------------------------|
| ZonedDateTifne<br>java.util.GregorianCalendar   | GregorianCalendar.<br>frofflfzonedDateTime) | cal.toZonedDateTimeO        |
| Instant<br>-» java.sql.Ti<br>stamp              | TineStamp.fron(instant)                     | timestamp.tolnstantf)       |
| LocalDateTine<br>*- java.sql.Tinestanp          | Timestamp.valueOf(localDateTime)            | timestamp.toLocalDateTine() |
| LocalDate<br>java.sql.Date                      | Date.valueOf(localDate)                     | date.toLocalDatel)          |
| LocalTime<br>java.sql.Time                      | Time.valueOf(localTime)                     | time.toLocalTiinel)         |
| DateTineFomatter<br>java, text. DateFo mat      | formatter.toForwatl)                        | 无                           |
| java.util.TimeZone<br>Zoneld                    | Timezone.getTineZone(id)                    | t imeZone. toZoneldO        |
| java.nio.file.attribute•FileTine<br>4-* Instant | FileT:ime .from( instant)                   | fileTiwe.toInstantO         |

*你 在 如何使 Java 8 日期和时 库来操作全世 日期和时 值了。下一 <sup>将</sup> 一步 如何为国 受众 。你将会 到如何以对客户 有意义 方式来格式化 序 消息、数字和 币 无 些客户 处世 何处。*

# *7 国 化*

- *▲ locale*
- *▲数字格式*
- *▲日期和时*
- *▲排序和 化*

- *▲消息格式化*
- *▲文本 人和 <sup>出</sup>*
- *▲ 源包*
- *▲ 一个完整 例子*

*世 丰富多彩 我们希望大 分居民 对你 件感兴 。一方 因 早已为我们打 了国家之 。另一方 如果你不去关注国 户 你 产品 应 情况就会受到 制。*

*Java 是 一 成为全 支持国 化 。从一开始 它就具备了 有 效 国 化所必 一个 性 使 Unicode来处 所有字 串。 于支持Unicode, 在Java 中 写 序来操作多 字 串变得异常方便。*

*多数 序员 为将 序 国 化 做 所有事情就是支持Unicode并在 户接口中 对消息 。但是 在本 你将会 到 国 化一个 序所 做 事情 不仅仅是提供 Unicode支持。在世 不同地方 日期、时 、 币 数字 格式 不 同。你 一 单 方法来为不同 单与按 名字、消息字 串和快捷 。*

*在本 中 我们将演 如何 写国 化 Java应 序以及如何将日期、时 、数字、 文本和图形 户 本地化 将演 Java提供 写国 化 序 工具。最后以一个完整 例子来作为本 束 它是一个 休 器 带有 、德 和中文 户 。*

#### *7.1 locale*

*当你 到一个 向国 市场 应 件时 它与其他 件最明显 区别就是 。其实 如果以 外在 不同来判断是不是 正 国 化就太 了 不同 国家可以使 同 但是为了使两个国家 户 满意 你 有很多工作 做。就像Oscar Wilde所 样 "我们 在 是每件东 和 国一样 当然 外"。*

#### *7.1.1为什么需要locale*

*当你提供 序 国 化 本时 所有 序消息 换为本地 。当然 接 户 文本是不够 有 多更 微 差异 例如 数字在 和德 中格式很不 同。对于德国 户 数字*

*123,456.78*

*应 显 为*

*123.456,78*

*小数点和十 制数 号分 是 反 在日期 显 上也有 似 变化。在 <sup>国</sup> 日期显 为月/日/年 有些不合 。德国使用的是更合理的顺序 即日/月/年 在中国 则使 <sup>年</sup>/月/日。因此 对于德国 <sup>户</sup> 日期*

*3/22/61*

#### *应 为*

*22.03.1961*

*当然 如果月份 名称被显式地写了出来 么 之 不同就显 易 了。 March 22, 1961*

#### *在德国应 成*

*22. Marz 1961*

#### *在中国则是*

*1961年3月22<sup>日</sup>*

*locale捕 了像上 偏好 征。无 何时 只 你 数字、日期、 币值以及其 他格式会随语言或地点发 变化的项 都需要使 locale感知的API。*

#### *7.1.2 指定 locale*

*locale 多 5个 分构成*

*<sup>1</sup>.一 2个或3个小写字母 例如en 英语 、de 德 和zh 中文 。 7-1展 了常用的代 。*

|         | 代  | 语苢         | 代  |
|---------|----|------------|----|
| Chinese | zh | Italian    | it |
| Danish  | da | Japanese   | ja |
| Dutch   | nl | Korean     | ko |
| English | en | Norwegian  | no |
| French  | fr | Portuguese | Pt |
| Finnish | fi | Spanish    | es |
| German  | de | Swedish    | SV |
| Greek   | el | Turkish    | tr |

*7-1<sup>常</sup> ISO-639-1 <sup>代</sup>*

- *2. 可 一段 本 字母大写 四个字母 例如Lain 拉丁文 、Cyrl 尔 文 和Hant 体中文 。 个 分很有 因为有些 例如塞尔 亚 可以 拉丁文 或 尔文书写 有些中文 更喜欢 体中文 不是 体中文。*
- *<sup>3</sup>. 可选的一个国家或地区 2个大写字母或3个数字表示 例如US 国 和CH 士 。 7-2展 了常 代 。*

| 国家            | 代 码 | 国家                | 代 码 |
|---------------|-----|-------------------|-----|
| Austria       | AT  | Japan             | JP  |
| Belgium       | BE  | Republic of Korea | KR  |
| Canada        | CA  | The Netherlands   | NL  |
| China         | CN  | Norway            | NO  |
| Denmark       | DK  | Portugal          | PT  |
| Finland       | FI  | Spain             | ES  |
| Germany       | DE  | Sweden            | SE  |
| Great Britain | GB  | Switzerland       | СН  |
| Ireland       | IE  | Turkey            | TR  |
| Italy         | IT  | United States     | US  |

表 7-2 常见的 ISO-3166-1 国家代码

- 4. 可选的一个变体,用于指定各种杂项特性,例如方言和拼写规则。变体现在已经很少使用了。过去曾经有一种挪威语的变体"尼诺斯克语",但是它现在已经用另一种不同的代码nn来表示了。过去曾经用于日本帝国历和泰语数字的变体现在也都被表示成了扩展(请参见下一条)。
- 5. 可选的一个扩展。扩展描述了日历(例如日本历)和数字(替代西方数字的泰语数字)等内容的本地偏好。Unicode 标准规范了其中的某些扩展,这些扩展应该以 u-和两个字母的代码开头,这两个字母的代码指定了该扩展处理的是日历(ca)还是数字(nu),或者是其他内容。例如,扩展 u-nu-thai 表示使用泰语数字。其他扩展是完全任意的,并且以 x-开头,例如 x-java。

locale 的规则在 Internet Engineering Task Force 的"Best Current Practices"备忘录 BCP 47 (http://tools.ietf.org/html/bcp47)中进行了明确阐述。

语言和国家的代码看起来有点乱,因为它们中有些是从本地语言导出的。德语在德语中是 Deutsch,中文在中文里是 zhongwen,因此它们分别是 de 和 zh。瑞士是 CH,这是从瑞士联邦的拉丁语 Confoederatio Helvetica 中导出的。

locale 是用标签描述的,标签是由 locale 的各个元素通过连字符连接起来的字符串,例如 en-US。

在德国,你可以使用 de-DE。瑞士有 4 种官方语言(德语、法语、意大利语和里托罗曼斯语)。在瑞士讲德语的人希望使用的 locale 是 de-CH。这个 locale 会使用德语的规则,但是货币值会表示成瑞士法郎而不是欧元。

如果只指定了语言,例如 de,那么该 locale 就不能用于与国家相关的场景,例如货币。 我们可以像下面这样用标签字符串来构建 Locale 对象:

Locale usEnglish = Locale.forLanguageTag("en-US");

toLanguageTag 方法可以生成用于给定 locale 的语言标签。例如,Locale.US.toLanguageTag() 生成的字符串是 "en-US"。

*为方便起见 有 多为各个国家 定义 Locale对*

*Locale.CANADA*

*Locale.CANADA\_FRENCH*

*Locale.CHINA*

*Locale.FRANCE* 

*Locale.GERMANY* 

*Locale.ITALY* 

*Locale.JAPAN* 

*Locale.KOREA* 

*Locale.UK*

*Locale.US*

*有 多 定义 Locale,它们只 定了语言而没有 定位*

*Locale.CHINESE*

*Locale.ENGLISH*

*Locale・ FRENCH* 

*Locale.GERMAN* 

*Locale.ITALIAN*

*Locale.JAPANESE*

*Locale.KOREAN*

*最后 态 getAvailableLocales方法会 回 Java 拟机 够 别 所有locale构 成 数 。*

*<sup>圍</sup> <sup>注</sup> 可以 Locale.getlSOLanguages() 取所有 <sup>代</sup> Locale.getlSOCountries() 取所有国家代 。*

# *7.1.3 默认 locale*

*Locale 态getDefault方法可以 得作为本地操作 一 分 存储 localeo可以调用setDefault来改变 Java locale,但是 改变只对你 序有效 不会对操作 产 影响。*

*有些操作 允 户为显 消息和格式化指定不同 locale。例如 活在 国 法 人 单是法 但是 币值是 元来 。*

*想 取 些偏好 可以调用*

*Locale displayLocale <sup>=</sup> Locale.getDefault(Locale.Category.DISPLAY); Locale forwatLocale <sup>=</sup> Locale.getDefault(Locale.Catego ry.FORMAT);*

- *注 在UNIX中 可以为数字、 币和日期分别 LCJJUMERIC、LC\_MONETARY<sup>和</sup> LCJIME 境变 来指定不同 locale。但是Java并不会关注 些 。*
- *提 为了测 你也 希望改变你的程序的默认locale,可以在启动 序时提供 和地域 性。比如 下 句将 locale 为de-CH*

*java -Duser.language=de -Duser.region=CH MyProgram*

#### 7.1.4 显示名字

一旦有了一个 locale, 你能用它做什么呢? 答案是它所能做的事情很有限。Locale 类中唯一有用的是那些识别语言和国家代码的方法, 其中最重要的一个是 getDisplayName, 它返回一个描述 locale 的字符串。这个字符串并不包含前面所说的由两个字母组成的代码, 而是以一种面向用户的形式来表现, 比如

German (Switzerland)

事实上,这里有一个问题,显示的名字是以默认的 locale 来表示的,这可能不太恰当。如果你的用户已经选择了德语作为首选的语言,那么你可能希望将字符串显示成德语。通过将 German locale 作为参数传递就可以做到这一点:代码

var loc = new Locale("de", "CH");
System.out.println(loc.getDisplayName(Locale.GERMAN));

#### 将打印出

Deutsch (Schweiz)

这个例子说明了为什么需要 Locale 对象。你把它传给 locale 感知的那些方法,这些方法将根据不同的地域产生不同形式的文本。在后面各节中你可以见到大量的例子。

● 警告:即使是像把字符串中的字母全部转换为小写或大写这样简单的操作,也可能是与 locale 相关的。例如,在土耳其 locale 中,字母 I 的小写是不带点的1。那些试图通过将字符串存储为小写格式来正则化字符串的程序对于土耳其客户来说就会显得很失败,因为 I 和带点的 i 没有相同的小写格式。一种好的做法是总是使用 toUpperCase 和 toLowerCase 的变体,这种变体会接受一个 Locale 参数。例如,试试下面的代码:

String cmd = "QUIT".toLowerCase(Locale.forLanguageTag("tr"));
 // "quit" with a dotless 1

当然,在土耳其,Locale.getDefault()产生的就是那里的locale, "QUIT".toLowerCase()与 "quit" 不同。

如果想要将英语字符串规范化为小写形式,那么就应该将英语的 locale 传递给 toLowerCase 方法。

- 這 注释: 你可以显式地指定输入/输出操作的 locale。
  - 当从 Scanner 读入数字时,可以用 useLocale 方法设置它的 locale。
  - String, format 和 PrintWriter, printf 方法也可以接受一个 Locale 参数。

#### API java.util.Locale

- Locale(String language)
- Locale(String language, String country)
- Locale(String language, String country, String variant)
   用给定的语言、国家和变量创建一个 locale。在新代码中不要使用变体,应该使用

IETF BCP 47 语言标签。

- static Locale forLanguageTag(String languageTag) 7
   构建与给定的语言标签相对应的 locale。
- static Locale getDefault()
   返回默认的 locale。
- static void setDefault(Locale loc)
   设定默认的 locale。
- String getDisplayName()
   返回一个在当前的 locale 中所表示的用来描述 locale 的名字。
- String getDisplayName(Locale loc)
   返回一个在给定的 locale 中所表示的用来描述 locale 的名字。
- String getLanguage()
   返回语言代码,它是两个小写字母组成的 ISO 639 代码。
- String getDisplayLanguage()
   返回在当前 locale 中所表示的语言名称。
- String getDisplayLanguage(Locale loc)
   返回在给定 locale 中所表示的语言名称。
- String getCountry()
   返回国家或地区代码,它是由两个大写字母组成的 ISO 3166 代码。
- static String[] getISOCountries()
- static Set<String> getISOCountries(Locale.IsoCountryCode type)
   获取所有两字母的国家或地区代码,或者所有 2、3、4个字母的国家或地区代码。 type参数是枚举常量 PART1\_ALPHA2、PART1\_ALPHA3 和 PART3 之一。
- String getDisplayCountry()
   返回在当前 locale 中所表示的国家或地区名。
- String getDisplayCountry(Locale loc)
   返回在给定 locale 中所表示的国家或地区名。
- String toLanguageTag() 7
   返回该 locale 的语言标签,例如 "de-CH"。
- String toString()
   返回 locale 的描述,包括语言和国家或地区,用下划线分隔(比如,"de\_CH")。应该只在调试时使用该方法。

#### 7.2 数字格式

我们已经提到了数字和货币的格式是高度依赖于 locale 的。Java 类库提供了一个格式器 (formatter) 对象的集合,它可以对 java.text 包中的数字值进行格式化和解析。

#### 7.2.1 格式化数字值

可以通过下面的步骤对特定 locale 的数字进行格式化:

- 1. 使用上一节的方法,得到 Locale 对象。
- 2. 使用一个"工厂方法"得到一个格式器对象。
- 3. 使用这个格式器对象来完成格式化和解析工作。

工厂方法是 NumberFormat 类的静态方法,它们接受一个 Locale 类型的参数。总共有 3 个工厂方法——getNumberInstance、getCurrencyInstance 和 getPercentInstance,这些方法返回的对象可以分别对数字、货币量和百分比进行格式化和解析。例如,下面显示了如何对德语中的货币值进行格式化。

```
Locale loc = Locale.GERMAN;
NumberFormat formatter = NumberFormat.getCurrencyInstance(loc);
double amt = 123456.78;
String result = formatter.format(amt);
```

#### 结果是

123.456,78 €

请注意,货币符号是€,而且位于字符串的最后。同时还要注意到小数点和十进制分隔符与其他语言中的情况是相反的。

Java 12 添加了两种风格的"紧凑"格式:短风格(123K)和长风格(123 thousand)。下面是获取短风格的代码:

formatter = NumberFormat.getCompactNumberInstance(loc, NumberFormat.Style.SHORT);

相反,如果想读取一个按照某个 locale 的惯用法而输入或存储的数字,那么就需要使用 parse 方法。比如,下面的代码解析了用户输入到文本框中的值。parse 方法能够处理小数点和分隔符以及其他语言中的数字。

TextField inputField;

```
NumberFormat fmt = NumberFormat.getNumberInstance();
// get the number formatter for default locale
Number input = fmt.parse(inputField.getText().strip());
double x = input.doubleValue();
```

parse 的返回类型是抽象类型 Number。返回的对象是一个 Double 或 Long 的包装器对象,这取决于被解析的数字是否是浮点数。如果不关心两者的差异,可以直接使用 Number 类的 doubleValue 方法来读取被包装的数字。

● 警告: Number 类型的对象并不能自动转换成相关的基本类型,因此,不能直接将一个Number 对象赋给一个基本类型,而应该使用 double Value 或 int Value 方法。

如果数字文本的格式不正确,该方法会抛出一个 ParseException 异常。例如,字符串以空白字符开头是不允许的(可以调用 trim 方法来去掉它)。但是,任何跟在数字之后的字符都将被忽略,所以这些跟在后面的字符是不会抛出异常的。

请注意,由 get Xxx Instance 工厂方法返回的类并非是 NumberFormat 类型的。NumberFormat 类型是一个抽象类,而我们实际上得到的格式器是它的一个子类。工厂方法只知道如何定位属于特定 locale 的对象。

可以用静态的 getAvailableLocales 方法得到一个当前支持的 locale 列表。这个方法返回一个 locale 数组,从中可以获得针对它们的数字格式器对象。

直 注释:可以使用 Scanner 来读取本地化的整数和浮点数。可以调用 useLocale 方法来设置 locale。

本节的示例程序可以让你体会到数字格式器的用法(参见图 7-1)。图上方的组合框包含所有带数字格式器的 locale,可以在数字、货币和百分率格式器之间进行选择。每次改变选择,文本框中的数字就会被重新格式化。在尝试了几种 locale 后,你就会对有这么多种方式来格式化数字和货币值而感到吃惊。也可以输入不同的数字并点击 Parse 按钮来调用 parse 方法,这个方法会尝试解析你输入的内容。如果解析成功,format 方法就会将结果显示出来。如果解析失败,文本框中会显示"Parse error"消息。

![](_page_104_Picture_5.jpeg)

图 7-1 NumberFormatTest 程序

程序清单7-1展示了这个数字格式探索器的通俗易懂的文本版本。

#### 程序清单 7-1 numberFormat/NumberFormatTest2.java

```
package numberFormat;
3 import java.text.*;
4 import java.util.*;
5 import util.*;
6
7
   * This program demonstrates formatting numbers under various locales.
    * @version 2.0 2021-09-22
   * @author Cav Horstmann
19
  public class NumberFormatTest2
12
   {
13
      public static void main(String[] args)
14
15
         Scanner in = new Scanner(System.in);
16
         var locales = (Locale[]) NumberFormat.getAvailableLocales().clone();
17
         Arrays.sort(locales, Comparator.comparing(Locale::getDisplayName));
18
         Locale loc = Choices.choose(in, locales, Locale::getDisplayName):
19
28
         var formatters = new LinkedHashMap<NumberFormat, String>();
21
         formatters.put(NumberFormat.getNumberInstance(loc), "Number");
22
         formatters.put(NumberFormat.getCompactNumberInstance(
23
               loc, NumberFormat.Style.SHORT), "Compact Short");
24
```

```
formatters.put(NumberFormat.getCompactNumberInstance(
25
                loc, NumberFormat.Style.LONG), "Compact Long");
26
27
          formatters.put(NumberFormat.getPercentInstance(loc), "Percent");
          formatters.put(NumberFormat.getCurrencyInstance(loc), "Currency");
28
29
         NumberFormat formatter = Choices.choose(in, formatters);
38
         String operation = Choices.choose(in, "Format", "Parse");
31
         if (operation.equals("Format"))
32
         {
33
             System.out.print("Enter a floating-point number to format: ");
34
             double number = in.nextDouble();
35
            System.out.println(formatter.format(number));
36
37
         else
38
          {
39
             System.out.print("Enter a floating-point number to parse: ");
             String text = in.next();
41
42
             try
                System.out.println(formatter.parse(text));
44
45
             catch (ParseException e)
46
47
                System.out.println("ParseException " + e.getMessage());
48
49
          }
50
51
52 }
```

#### API java.text.NumberFormat

- static Locale[] getAvailableLocales()
   返回一个 Locale 对象的数组,其成员为可用的 NumberFormat 格式器。
- static NumberFormat getNumberInstance()
- static NumberFormat getNumberInstance(Locale 1)
- static NumberFormat getCurrencyInstance()
- static NumberFormat getCurrencyInstance(Locale 1)
- static NumberFormat getPercentInstance()
- static NumberFormat getPercentInstance(Locale 1)
   为当前或给定的 locale 提供处理数字、货币量或百分比的格式器。
- static NumberFormat getCompactNumberInstance() 12
- static NumberFormat getCompactNumberInstance(Locale locale, NumberFormat.Style formatStyle)
   12

返回当前 locale 中的 SHORT 风格的紧凑数字格式器,或者返回给定 locale 和风格(SHORT 或 LONG)的紧凑数字格式器。

- String format(double x)
- String format(long x)

对给定的浮点数或整数进行格式化并以字符串的形式返回结果。

Number parse(String s)

解析给定的字符串并返回数字值,如果输入字符串描述了一个浮点数,返回类型就是 Double, 否则返回类型就是 Long。字符串必须以一个数字开头,以空白字符开头是不允许的。数字之后可以跟随其他字符,但它们都将被忽略。解析失败时抛出 ParseException 异常。

- void setParseIntegerOnly(boolean b)
- boolean isParseIntegerOnly()
   设置或获取一个标志,该标志指示这个格式器是否应该只解析整数值。
- void setGroupingUsed(boolean b)
- boolean isGroupingUsed()
   设置或获取一个标志,该标志指示这个格式器是否会添加和识别十进制分隔符(比如,100,000)。
- void setMinimumIntegerDigits(int n)
- int getMinimumIntegerDigits()
- void setMaximumIntegerDigits(int n)
- int getMaximumIntegerDigits()
- void setMinimumFractionDigits(int n)
- int getMinimumFractionDigits()
- void setMaximumFractionDigits(int n)
- int getMaximumFractionDigits() 设置或获取整数或小数部分所允许的最大或最小位数。

#### 7.2.2 DecimalFormat 类

在大多数 locale 中,在上一节中看到的各个 NumberFormat 工厂方法都会返回 Decimal-Format 类的一个实例。这个类描述了世界各地的各种格式化机制。你可以修改现有对象的每个设置项,也可以创建全新的格式器。模式语法使这种设置变得更简便了。

模式描述了必需的和可选的数字位数,以及正数和负数的前缀与后缀。还有一些看起来 更深奥的设置,详情请查看表 7-3。

| <b>国州</b> 夕                   | 44 44        | <b>#</b>                          |
|-------------------------------|--------------|-----------------------------------|
| 属性名                           | 描述           | 模 式                               |
| groupingSize                  | 群组在一起的整数数字位数 |                                   |
| 3                             | (通常是3或4)     | 数,例如 #,### 表示群组尺寸为 3              |
| minimum/maximumFractionDigits | 小数部分最少和最大的位数 | 在小数部分中使用必需 (θ) 和可选 (#) 的位数: .00## |
| minimumIntegerDigits          | 整数部分最少的位数    | 整数中必需 (0) 的位数: 000                |

表 7-3 Decimal Format 的屋性

(绫)

| 属性名                                              | 描述                            | 模式                                                                      |
|--------------------------------------------------|-------------------------------|-------------------------------------------------------------------------|
| maximumIntegerDigits                             | 最大的整数位数                       | 使用指数表示法时,整数部分允许出现的#的数量,例如###,##0.00E0。如果不使用指数表示法,则不能在模式中设置该属性           |
| -                                                | 指数部分最少的位数                     | 在 E 部分中使用 0 的位数: #.00E00                                                |
| multiplier                                       | 百分号和千分号                       | %表示百分号,‰ (U+2030)表示千分号                                                  |
| positivePrefix/Suffix,negative-<br>Prefix/Suffix | 正数和负数的前缀与后缀                   | 用字面值表示的前缀和后缀包围模式中的正数或负数部分。例如,在 +#0.00;(#)中,+表示正数的前缀,且没有指定后缀,用圆括号将负数括了起来 |
| decimalSeparatorAlwaysShown                      | 如果在小数部分为θ时也显示<br>分隔符,则设置为true | 不能在模式中设置                                                                |

#### 考虑下面的例子:

var formatter = new DecimalFormat("0.00;(#)");

模式中的分号将正数和可选的负数部分分隔开。在正数部分中,我们看到在其整数部分至少有一位数字,而在小数部分至少有两位数字。所有的数字都要满足这两点,无论其符号是正还是负。负数使用了会计模式,即包含一个前缀(和一个后缀)。

前缀和后缀可以包含一个货币符号 ¤(U+00A4), 用来表示货币符号应该出现的位置。

如果需要在前缀或后缀中插入特殊字符,需要在其前面插入一个单引号。例如,前缀 '# 表示字面哈希符号,而 o''clock 中包含一个单引号。

数字位、分隔符和其他各种数字部分的实际符号可以从 DecimalFormatSymbols 对象中获取,你也可以自定义该对象,表 7-4 列出了它的属性。

属性 类型 描述 像"\$"和"EUR"这样的字符串,用于包含货币符号 currencySymbol String n 的前缀或后缀中 decimalSeparator, monetaryDecimalSeparator 小数分隔符, 用于数字或货币值 char exponentSeparator String 在指数 E部分之前的字符串,通常是"E" groupingSeparator, monetaryGroupingSeparator 群组分隔符, 用于数字或货币值 char (Java 15 以后才支持) 用于格式化的字符串: Double.POSITIVE INFINITY、Double. infinity, naN String NEGATIVE INFINITY 和 Double.NaN internationalCurrencySymbol 遵循 ISO 4217 标准的货币符号--请查看 7.2.3 节 String char 在未指定负数模式的情况下使用的负号 minusSign percent, perMill 用于百分号和千分号的符号 char 用于数字位0的字符。其他数字位为后续的9个 zeroDigit char Unicode 字符

表 7-4 DecimalFormatSymbols 的属性

*例如 假 你希望无 使 什么locale, 国 格展 数字 其中 作 分 . 作小数分 。此时 可以 定义DecimalFormatSymbols和格式器。*

```
DecimalForinatSymbols symbols = new DecimalFoanatSymbols(loc);
symbols•setGroupingSeparator(
symbols.setDecimalSeparator(
DecimalFormat formatter = (DecimalFormat) NumberFormat.getNumberlnstance(loc);
formatter.setDecimalFonnatSymbolsfsymbols);
```

#### *7.2.3 <sup>币</sup>*

*为了格式化 币值 可以使 NumberFormat.getCurrencylnstance方法。但是 个方法 灵活性不好 它 回 是一个只 对一 币 格式器。假 你为一个 国客户准备了一 张货物单 单中有些 是 元 有些是 欧元 此时 你不 只是使 两 格式器*

```
NumberFormat doUarFormatter = NumberFormat.getCurrencylnstance(Locale.US);
NumberFormat euroFormatter = NumberFormat.getCurrencylnstance(Locale.GERMANY);
```

*是因为 样一来 你 发 来 常奇怪 有些 格式像\$100,000,另一些 则像100.000 € (注意 欧元值使 小数点 不是 号作为分 )。*

*处 样 情况 应 使 Currency 来控制 格式器处 币。可以 将一个 币标 传 态 Currency.getlnstance方法来得到一个Currency对 然后对每一个格 式器都调用setcurrency方法。下 展 了如何为你 国客户 欧元 格式*

*NumberFormat euroFormatter <sup>=</sup> NumberFormat.getCurrencylnstance(Locale.US); euroFormatter.setCurrency(Currency.getInstance("EUR"));*

*币标 ISO4217定义 可参 https://www.iso.org/iso-4217-currency-codes.html<sup>o</sup> 7-5提供了其中 一 分。*

| 币值 | 标   | 币代号 | 币值   | 标识符 | 币代号 |
|----|-----|-----|------|-----|-----|
| 元  | USD | 840 | 人民币  | CNY | 156 |
| 欧元 | EUR | 978 | 印度卢比 | INR | 356 |
|    | GBP | 826 | 卢布   | RUB | 643 |
| 日元 | JPY | 392 |      |     |     |

*7-5 币标识符*

#### *vi| java.util.Currency*

- *• static Currency getInstance(String currencyCode)*
- *• static Currency getInstance(Locale locale) 回与 定 ISO 4217 币代号或 定 locale中 国家和地区 对应 Currency 对 。*
- *• String toStringO*

- 316
  - String getCurrencyCode()
  - String getNumericCode() 7
  - String getNumericCodeAsString() 9
     获取该货币的 ISO 4217 字母或数字代码。
  - String getSymbol()
  - String getSymbol(Locale locale) 根据默认或给定的 locale 得到该货币的格式化符号。比如美元的格式化符号可能是 "\$" 或 "US\$", 具体是哪种形式取决于 locale。
  - int getDefaultFractionDigits()
     获取该货币小数点后的默认位数。
  - static Set<Currency> getAvailableCurrencies() 7
     获取所有可用的货币。

#### 7.3 日期和时间

当格式化日期和时间时,需要考虑 4 个与 locale 相关的问题:

- 月份和星期应该用本地语言来表示。
- 年、月、日的顺序要符合本地习惯。
- 公历可能不是本地首选的日期表示方法。
- 必须要考虑本地的时区。

LONG

FULL

java.time 包中的 DateTimeFormatter 类可以处理这些问题。首先挑选表 7-6 中所示的一种格式风格,然后获取一个格式器:

表 7-6 日期和时间的格式化风格

```
FormatStyle style = . . .; // One of FormatStyle.SHORT, FormatStyle.MEDIUM, . . . DateTimeFormatter dateFormatter = DateTimeFormatter.ofLocalizedDate(style); DateTimeFormatter timeFormatter = DateTimeFormatter.ofLocalizedTime(style); DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofLocalizedDateTime(style); // or DateTimeFormatter.ofLocalizedDateTime(style1, style2)
```

风格 日期 时 SHORT 7/16/69 9:32 AM MEDIUM Jul 16, 1969 9:32:00 AM

July 16, 1969

Wednesday, July 16, 1969

这些格式器都会使用当前的 locale。为了使用不同的 locale,需要使用 withLocale 方法:

9:32:00 AM EDT in en-US, 9:32:00 MSZ in de-DE

9:32:00 AM EDT in en-US, 9:32 Uhr MSZ in de-DE

(只用于 ZonedDateTime)

(只用于 ZonedDateTime)

DateTimeFormatter dateFormatter =

DateTimeFormatter.ofLocalizedDate(style).withLocale(locale);

现在你可以格式化 LocalDate、LocalDateTime、LocalTime 和 ZonedDateTime 了:

ZonedDateTime appointment = . . .;

String formatted = formatter.format(appointment);

直 注释: 这里我们使用的是 java.time 包中的 DateTimeFormatter。还有一种来自 Java 1.1 的遗留的 java.text.DateFormatter 类,它操作的是 Date 和 Calendar 对象。

可以使用 LocalDate 、LocalDateTime、LocalTime 和 ZonedDateTime 的静态 parse 方法之一来解析字符串中的日期和时间:

LocalTime time = LocalTime.parse("9:32 AM", formatter);

这些方法不适合解析人类的输入,至少不适合解析未做预处理的人类输入。例如,用于美国的短时间格式器可以解析 "9:32 AM",但是解析不了 "9:32 AM" 和 "9:32 am"。

● 警告:日期格式器可以解析不存在的日期,例如 November 31,它会将这种日期调整 为给定月份的最后一天。

有时,你需要显示星期和月份的名字,例如在日历应用中。此时可以调用 DayOfWeek 和 Month 枚举的 getDisplayName 方法:

for (Month m : Month.values())

System.out.println(m.getDisplayName(textStyle, locale) + " ");

表 7-7 展示了文本风格,其中 STANDALONE 版本用于格式化日期之外的显示。例如,在芬兰语中,一月在日期中是"tammikuuta",但是单独显示时是"tammikuu"。

| 风格                         | 示 例     |
|----------------------------|---------|
| FULL / FULL_STANDALONE     | January |
| SHORT / SHORT_STANDALONE   | Jan     |
| NARROW / NARROW_STANDALONE | J       |

表 7-7 java.time.format.TextStyle 枚举

直 注释:星期的第一天可以是星期六、星期日或星期一,这取决于 locale。你可以像下面这样获取星期的第一天:

DayOfWeek first = WeekFields.of(locale).getFirstDayOfWeek();

程序清单 7-2 展示了如何在实际中使用 DateFormat 类,用户可以选择一个 locale 并看看日期和时间在世界上的不同地区是如何格式化的。

#### 程序清单 7-2 dateFormat/DateTimeFormatTest2.java

package dateFormat;

2

3 import java.text.\*;

```
4 import java.time.*;
5 import java.time.format.*;
6 import java.util.*;
7 import util.*;
8
9 /**
    * This program demonstrates formatting dates under various locales.
10
    * @version 2.0 2021-09-23
11
   * @author Cay Horstmann
13
14 public class DateTimeFormatTest2
15 {
      public static void main(String[] args)
16
      {
17
         Scanner in = new Scanner(System.in);
18
         var locales = (Locale[]) NumberFormat.getAvailableLocales().clone();
19
         Arrays.sort(locales, Comparator.comparing(Locale::getDisplayName));
28
         Locale loc = Choices.choose(in, locales, Locale::getDisplayName);
21
         FormatStyle style = Choices.choose(in, FormatStyle.class,
22
                "Short", "Medium", "Long", "Full");
23
         String type = Choices.choose(in, "Date", "Time", "Date and Time");
24
25
         if (type.equals("Date"))
26
27
            DateTimeFormatter formatter = DateTimeFormatter.ofLocalizedDate(
28
                   style).withLocale(loc);
29
            System.out.println(formatter.format(LocalDate.now()));
38
            System.out.print("Enter another date: ");
31
            String input = in.nextLine();
32
            LocalDate date = LocalDate.parse(input, formatter);
33
            System.out.println(formatter.format(date));
34
35
         else if (type.equals("Time"))
36
37
            DateTimeFormatter formatter = DateTimeFormatter.ofLocalizedTime(
38
                   style).withLocale(loc);
39
            System.out.println(formatter.format(LocalTime.now()));
48
             System.out.print("Enter another time: ");
41
            String input = in.nextLine():
42
            LocalTime time = LocalTime.parse(input, formatter);
            System.out.println(formatter.format(time));
44
         }
45
         else
46
47
             DateTimeFormatter formatter = DateTimeFormatter.ofLocalizedDateTime(
48
                   style).withLocale(loc);
49
             System.out.println(formatter.format(ZonedDateTime.now()));
50
             System.out.print("Enter another date and time: ");
51
             String input = in.nextLine();
52
             ZonedDateTime dateTime = ZonedDateTime.parse(input, formatter);
53
             System.out.println(formatter.format(dateTime));
54
55
       }
56
57 }
```

图 7-2 显示了该程序的 GUI 版本,它包含在随书附带的代码中。你需要安装中文字体,这样才能显示中文字符。

![](_page_112_Picture_2.jpeg)

图 7-2 DateFormatTest 程序

#### API java.time.format.DateTimeFormatter

- static DateTimeFormatter ofLocalizedDate(FormatStyle dateStyle)
- static DateTimeFormatter ofLocalizedTime(FormatStyle dateStyle)
- static DateTimeFormatter ofLocalizedDateTime(FormatStyle dateTimeStyle)
- static DateTimeFormatter ofLocalizedDate(FormatStyle dateStyle, FormatStyle timeStyle) 返回用指定的风格格式化日期、时间或日期和时间的 DateTimeFormatter 实例。
- DateTimeFormatter withLocale(Locale locale)
   返回当前格式器的具有给定 locale 的副本。
- String format(TemporalAccessor temporal)
   返回格式化给定日期/时间所产生的字符串。

```
java.time.LocalDate 8
java.time.LocalDateTime 8
java.time.ZonedDateTime 8
```

static Xxx parse(CharSequence text, DateTimeFormatter formatter)
 解析给定的字符串并返回其中描述的 LocalDate、LocalTime、LocalDateTime 或 ZonedDate-Time。如果解析不成功,则抛出 DateTimeParseException 异常。

#### 7.4 排序和规范化

大多数程序员都知道如何使用 String 类中的 compareTo 方法对字符串进行比较。但是,当与人类用户交互时,这个方法就不是很有用了。compareTo 方法使用的是字符串的 UTF-16 编码值,这会导致很荒唐的结果,即使在英文比较中也是如此。比如,下面的 5 个字符串进行排序的结果为:

America Zulu able zebra Ångström

按照字典中的顺序, 你希望将大写和小写看作是等价的。对于一个说英语的读者来说,

#### 期望的排序结果应该是:

able

America

Ångström

zebra

Zulu

但是,这种顺序对于瑞典用户是不可接受的。在瑞典语中,字母 A 和字母 A 是不同的,它应该排在字母 Z 之后!就是说,瑞典用户希望排序的结果是:

able

America

zebra

Zulu

Angström

为了获得 locale 敏感的比较器,可以调用静态的 Collator.getInstance 方法:

Collator coll = Collator.getInstance(locale);

words.sort(coll); // Collator implements Comparator<Object>

因为 Collator 类实现了 Comparator 接口,因此,可以传递一个 Collator 对象给 list. sort (Comparator) 方法来对一组字符串进行排序。

排序器有几个高级设置项。你可以设置排序器的强度来选择不同的排序行为。字符间的差别可以被分为首要的(primary)、其次的(secondary)和再次的(tertiary)。比如,在英语中,"A"和"Z"之间的差别被归为首要的,而"A"和"A"之间的差别是其次的,"A"和"a"之间的差别是再次的。

如果将排序器的强度设置成 Collator.PRIMARY,那么排序器将只关注 primary 级的差别。如果设置成 Collator.SECONDARY,排序器将把 secondary 级的差别也考虑进去。就是说,两个字符串在"secondary"或"tertiary"强度下更容易被区分开来,如表 7-8 所示。

| 首 要                 | 其 次                 | 再 次                 |
|---------------------|---------------------|---------------------|
| Angstrom = Ångström | Angstrom ≠ Ångström | Angstrom ≠ Ångström |
| Able = able         | Able = able         | Able ≠ able         |

表 7-8 不同强度下的排序 (英语 locale)

如果强度被设置为 Collator. IDENTICAL,则不允许有任何差别。这种设置在与排序器的另一种具有相当技术性的设置即分解模式 (decomposition mode) 联合使用时,显得非常有用。我们接下来将讨论分解模式。

偶尔我们会碰到一个字符或字符序列在被描述成 Unicode 时有多种方式的情况。例如,"A"可以是 Unicode 字符 U+00C5,或者可以表示成普通的 A(U+0065)后跟<sup>。</sup>("上方组合环",U+030A)。也许让你更吃惊的是,字母序列"ffi"可以用代码 U+FB03 描述成单个字符"拉丁小连字ffi"。(有人会说这是表示方法的不同,不应该因此产生不同的 Unicode 字符,但规则不是我们定的。)

Unicode 标准对字符串定义了四种规范化形式 (normalization form): D、KD、C和KC。

请查看 http://www.unicode.org/unicode/reports/tr15/tr15-23.html 以了解详细信息。在规范化形式 C 中,重音符号总是组合的。例如,A 和上方组合环。被组合成了单个字符 Å。在规范化形式 D 中,重音字符被分解为基字符和组合重音符。例如,A 就被转换成由字母 A 和上方组合环。构成的序列。规范化形式 KC 和 KD 也会分解字符,例如连字或商标符号。

我们可以选择排序器所使用的规范化程度: Collator.NO\_DECOMPOSITION表示不对字符串做任何规范化,这个选项处理速度较快,但是对于以多种形式表示字符的文本就不适用了;默认值 Collator.CANONICAL\_DECOMPOSITION使用规范化形式 D,这对于包含重音但不包含连字的文本是非常有用的形式;最后是使用规范化形式 KD的"完全分解"。请参见表 7-9 中的示例。

| 不分解             | 规范分解                          | 完全分解  |
|-----------------|-------------------------------|-------|
| Å ≠ A°          | Å=A°                          | Å=A°  |
| $^{TM} \neq TM$ | $^{\text{TM}} \neq \text{TM}$ | TM=TM |

表 7-9 分解模式之间的差异

让排序器去多次分解一个字符串是很浪费的。如果一个字符串要和其他字符串进行 多次比较,可以将分解的结果保存在一个排序键对象中。getCollationKey 方法返回一个 CollationKey 对象,可以用它来进行更进一步、更快速的比较操作。下面是一个例子:

String a = . . .;

CollationKey aKey = coll.getCollationKey(a);

if(aKey.compareTo(coll.getCollationKey(b)) == 0) // fast comparison

最后,你有可能在不需要进行排序时,也希望将字符串转换成其规范化形式。例如,在将字符串存储到数据库中,或与其他程序进行通信时。java.text.Normalizer类实现了对规范化的处理。例如:

String name = "Angström";

String normalized = Normalizer.normalize(name, Normalizer.Form.NFD);
// uses normalization form D

上面的字符串规范化后包含 10 个字符, 其中"Å"和"ö"被替换成了"A°"和"o""序列。

但是,这种形式通常并不是用于存储或传输的最佳形式。规范化形式 C 首先进行分解,然后将重音按照标准化的顺序组合在后面。根据 W3C 的标准,这是用于在因特网上进行数据传输的推荐模式。

程序清单 7-3 中的程序让你体验了一下比较排序。本书附带的代码中还包括一个 GUI 版本。你可以向文本框中输入一个词然后点击 Add 按钮把它添加到一个单词列表中。每当添加一个单词,或选择 locale、强度或分解模式时,列表中的单词就会被重新排列。符号=表示这两个词被认为是等同的(参见图 7-3)。

![](_page_114_Picture_15.jpeg)

图 7-3 CollationTest 程序

locale 名字的排列顺序,是用默认 locale 的排序器进行排序而产生的顺序。如果用美国英语 locale 运行这个程序,即使逗号的 Unicode 值比右括号的 Unicode 值大,"Norwegian (Norway, Nynorsk)"也会显示在"Nor-wegian (Norway)"的前面。

#### 程序清单 7-3 collation/CollationTest2.java

```
package collation;
2
3 import java.text.*;
4 import java.util.*;
5 import util.*;
7 /**
    * This program demonstrates collating strings under various locales.
    * @version 2.0 2021-09-23
    * @author Cay Horstmann
10
11
12 public class CollationTest2
13 {
      public static void main(String[] args)
14
15
         Scanner in = new Scanner(System.in);
16
         var locales = (Locale[]) NumberFormat.getAvailableLocales().clone();
17
         Arrays.sort(locales, Comparator.comparing(Locale::getDisplayName));
18
         Locale loc = Choices.choose(in, locales, Locale::getDisplayName);
19
28
         Collator coll = Collator.getInstance(loc);
21
         int strength = Choices.choose(in, Collator.class,
22
               "Primary", "Secondary", "Tertiary", "Identical");
23
         int decomposition = Choices.choose(in, Collator.class,
24
               "Canonical Decomposition", "Full Decomposition", "No Decomposition");
25
26
         List<String> strings = new ArrayList<>();
27
         strings.add("America");
28
         strings.add("able");
29
         strings.add("Zulu");
38
         strings.add("zebra");
31
         strings.add("\u00C5ngstr\u00F6m");
32
         strings.add("A\u030angstro\u0308m");
33
         strings.add("Angstrom");
34
         strings.add("Able");
35
         strings.add("office");
36
37
         strings.add("o\uFB03ce");
         strings.add("Java\u2122");
38
         strings.add("JavaTM");
30
         coll.setStrength(strength);
41
         coll.setDecomposition(decomposition);
47
43
         strings.sort(coll);
44
45
         for (int i = 0; i < strings.size(); i++)
46
47
             String s = strings.get(i):
48
```

```
if (i > θ && coll.compare(s, strings.get(i - 1)) == θ)
```

#### API java.text.Collator

- static Locale[] getAvailableLocales()
   返回 Locale 对象的一个数组,该 Collator 对象可用于这些对象。
- static Collator getInstance()
- static Collator getInstance(Locale 1)
   为默认或给定的 locale 返回一个排序器。
- int compare(String a, String b)
   如果a在b之前,则返回负值;如果它们相等,则返回0;其他情况则返回正值。
- boolean equals(String a, String b)
   如果 a 和 b 相等,则返回 true,否则返回 false。
- void setStrength(int strength)
- int getStrength()

设置或获取排序器的强度。更强的排序器可以区分更多的词。强度的值可以是Collator.PRIMARY、Collator.SECONDARY和Collator.TERTIARY。

- void setDecomposition(int decomp)
- int getDecompositon()

设置或获取排序器的分解模式。分解越细,判断两个字符串是否相等时就越严格。分解的等级值可以是 Collator.NO\_DECOMPOSITION、Collator.CANONICAL\_DECOMPOSITION和 Collator.FULL DECOMPOSITION。

CollationKey getCollationKey(String a)
 返回一个排序器键,这个键包含一个对一组字符按特定格式分解的结果,可以快速地和其他排序器键进行比较。

#### API java.text.CollationKey

 int compareTo(CollationKey b)
 如果这个键在 b 之前,则返回一个负值;如果两者相等,则返回 0;其他情况则返回 正值。

#### API java.text.Normalizer

static String normalize(CharSequence str, Normalizer.Form form)
 返回 str 的规范化形式, form 的值是 ND、NKD、NC 或 NKC 之一。

#### 7.5 消息格式化

Java 类库中有一个用来对包含变量部分的文本进行格式化的 MessageFormat 类,它的格式化方式与用 printf 方法进行格式化很类似,但是它支持 locale,并且可以对数字和日期进行格式化。我们将在以下各节中审视这种机制。

#### 7.5.1 格式化数字和日期

下面是一个典型的消息格式化字符串:

"On {2}, a {0} destroyed {1} houses and caused {3} of damage."

括号中的数字是占位符,可以用实际的名字和值来替换它们。使用静态方法 Message-Format.format 可以用实际的值来替换这些占位符。它是一个"varargs"方法,所以可以通过下面的方法提供参数:

String msg

= MessageFormat.format("On {2}, a {0} destroyed {1} houses and caused {3} of damage.",
 "hurricane", 99, new GregorianCalendar(1999, 0, 1).getTime(), 10.0E8);

在这个例子中, 占位符 {0} 被 "hurricane" 替换, {1} 被 99 替换, 以此类推。

上述例子的结果是下面的字符串:

On 1/1/99 12:00 AM, a hurricane destroyed 99 houses and caused 100,000,000 of damage.

这只是开始, 离完美还有距离。我们不想将时间显示为"12:00 AM", 而且我们想将造成的损失量打印成货币值。通过为占位符提供可选的格式, 就可以做到这一点:

"On {2,date,long}, a {0} destroyed {1} houses and caused {3,number,currency} of damage."

这段示例代码将打印出:

On January 1, 1999, a hurricane destroyed 99 houses and caused \$100,000,000 of damage.

一般来说,占位符索引后面可以跟一个类型(type)和一个风格(style),它们之间用逗号隔开。类型可以是:

number

time

date

choice

如果类型是 number, 那么风格可以是

integer

currency

percent

或者是一个 DecimalFormat 模式,如 \$,##0。(关于格式的更多信息,可参见 7.2.2 节 Decimal-Format 类。)

如果类型是 time 或 date, 那么风格可以是

short medium long full

或者是一个日期格式模式,如 yyyy-MM-dd。(关于格式的更多信息,可参见 SimpleDateFormat 类的文档。)

● 警告: 静态的 MessageFormat.format 方法使用当前的 locale 对值进行格式化。要想用任意的 locale 进行格式化,还有一些工作要做,因为这个类还没有提供任何可以使用的"varargs"方法。你需要把将要格式化的值置于 0bject[] 数组中,就像下面这样:

var mf = new MessageFormat(pattern, loc);
String msg = mf.format(new Object[] { values });

#### API java.text.MessageFormat

- MessageFormat(String pattern)
- MessageFormat(String pattern, Locale loc)
   用给定的模式和 locale 构建一个消息格式对象。
- void applyPattern(String pattern)
   给消息格式对象设置特定的模式。
- void setLocale(Locale loc)
- Locale getLocale()

设置或获取消息中占位符所使用的 locale。这个 locale 仅仅被通过调用 applyPattern 方法所设置的后续模式使用。

- static String format(String pattern, Object... args)
   通过使用 args[i] 作为占位符 {i} 的输入来格式化 pattern 字符串。
- StringBuffer format(Object args, StringBuffer result, FieldPosition pos)
   格式化 MessageFormat 的模式。args 参数必须是一个对象数组。被格式化的字符串会被附加到 result 末尾,并返回 result。如果 pos 等于 new FieldPosition (MessageFormat.Field.ARGUMENT),就用它的 beginIndex 和 endIndex 属性值来设置替换占位符{1}的文本位置。如果不关心位置信息,可以将它设为 null。

#### API java.text.Format

String format(Object obj)
 按照格式器的规则格式化给定的对象,这个方法将调用 format(obj,new StringBuffer(), new FieldPosition(1)).toString()。

#### 7.5.2 选择格式

让我们仔细地看看前面一节所提到的模式:

"On {2}, a {0} destroyed {1} houses and caused {3} of damage."

如果我们用 "earthquake" 来替换代表灾难的占位符 {0},那么在英语中,这句话的语法就不正确了。

On January 1, 1999, a earthquake destroyed . . .

这说明, 我们真正希望的是将冠词"a"集成到占位符中去:

"On {2}, {0} destroyed {1} houses and caused {3} of damage."

这样我们就应该用 "a hurricane" 或 "an earthquake" 来替换 {0}。当消息需要被翻译成某种语言,而该语言中的词会随词性的变化而变化时,这种替换方式特别适用。比如,在德语中,模式可能是:

"{0} zerstörte am {2} {1} Häuser und richtete einen Schaden von {3} an."

这样,占位符将被正确地替换成冠词和名词的组合,比如 "Ein Wirbelsturm" 或 "Eine Natur-katastrophe"。

让我们来看看参数 {1}。如果灾难的后果不严重, {1} 的替换值可能是数字 1, 消息就变成: On January 1, 1999, a mudslide destroyed 1 houses and . . .

我们当然希望消息能够随占位符的值而变化,这样就能根据具体的值形成

no houses one house 2 houses

choice 格式化选项就是为了这个目的而设计的。

- 一个选择格式是由一个序列对构成的,每一个序列对包括:
- 一个下限 (lower limit)
- 一个格式字符串 (format string)

下限和格式字符串由一个#符号分隔,对与对之间由符号 | 分隔。例如,

{1,choice,0#no houses|1#one house|2#{1} houses}

表 7-10 显示了格式字符串对 {1} 的不同值产生的作用。

| {1} | 结 果         | {1} | 结 果         |
|-----|-------------|-----|-------------|
| 0   | "no houses" | 3   | "3 houses"  |
| 1   | "one house" | -1  | "no houses" |

表 7-10 由选择格式进行格式化的字符串

为什么在格式字符串中两次用到了 {1}? 当消息格式将选择格式应用于占位符 {1} 而且替换值是 2 时,选择格式会返回 "{1} houses"。这个字符串由消息格式再次格式化,并将这次的结果和上一次的叠加。

*0 <sup>注</sup> 个例子 <sup>明</sup> 择格式 有些 涂了。如果你有3个格式字 <sup>串</sup> <sup>就</sup> 两个下 来分 它们。一 来 你 下 數 比格式字 串数 少1。就像 你在 7-10中 到 MessageFormat 将忽 一个下 。*

*如果 个 意 到下 只在两个 择之 出 么 法就 清楚得多 比如*

*no houses|1|one house|2|{l} houses // not the actual format*

*可以使 < 号来 如果替换值严格小于下 <sup>则</sup> <sup>中</sup> <sup>个</sup> <sup>择</sup> 。*

*也可以使 <sup>名</sup>(Unicode<sup>中</sup> <sup>代</sup> <sup>是</sup>\u2264 )来实 和# <sup>同</sup> 效果。如果愿意 可以将 一个下 值定义为-oo (Unicode代 是-\u221E)。*

*例如*

*• <»<no houses|8<one house|2^{l} houses*

#### *或 使 Unicode 义字*

*•\u221E<no houses|6<one house|2\u2264{l} houses*

*我们来 束 然灾害 场景。如果我们将 择字 串放到原始消息字 串中 么会 得到下 格式化指令*

*String pattern = "On {2,date,long}, {8} destroyed {1,choice,6#no houses|l#one house|2\*(1} houses}' <sup>+</sup> "and caused {3,number,currency} of damage.';*

#### *在德 中 即*

*String pattern*

*="{0} zerstorte am {2,date,long} {1,choice,9#kein Haus|l#ein Haus|2#{l} Hauser}" <sup>+</sup> "und richtete einen Schaden von {3,number,currency} an.";*

*同 。可以 格式字 串中占位 序来处 单 序 改变。*

*注意 在德 中 序和 中是不同 但是你传 format方法 对 数 是*

## *7.6文本 入和 <sup>出</sup>*

*众所周 Java 是完全基于Unicode 。但是 Windows和Mac OS X<sup>仍</sup> 旧支持 字 机制 例如 欧国家 Windows-1252和Mac Roman。因此 与 户 通过文本沟 并非看上去 么 单。下 各 将 你可 会 到 各 复杂情况。*

#### *7.6.1文本文件*

*当今最好是使 UTF-8来存储和加 文本文件 但是你可 操作 文件。如果你 知道遗留文件所希望使用的字符编码机制 么可以在 写文本文件时指定它*

*var out = new PrintWriter(filename, "Windows-1252");*

*如果想要获得可用的最佳编码机制 可以 下 来 得"平台 机制"*

*Charset platformEncoding <sup>=</sup> Charset.defaultCharset();*

#### *7.6.2 <sup>束</sup>*

*不是locale 是平台 。在Windows中 文本文件希望在每 末尾使 \r\n, 基于UNIX <sup>只</sup> 一个\n<sup>字</sup> 。当今 大多数Windows <sup>序</sup> 可以处 只有 一个\n 情况 一个 例外是 事本。如果" 户可以在你 <sup>应</sup> 所产 文本文件上双击 并在 事本中浏 它"对你来 常 么你就 保 文本文件使 了正 束 。*

*任何 printin方法写人 将是 正 止 。唯一 是你是否打印了包含\n 字 。它们不会 动修改为平台 束 。*

*与在字 串中使 \n不同 可以使 printf和%n格式 明 来产 平台 关 束 。例如*

*out .printf( "HeUo%nWorld%n");*

*会在Windows上产*

*HeUo\r\nWorld\r\n*

*在其他所有平台上产*

*HeUo\nWorld\n*

#### *7.6.3控制台*

*如果你 <sup>写</sup> 序是 System.in/System.out或System.console()<sup>与</sup> 户交互 么就 不得不 对控制台使 字 机制与Charset.defaultCharsetf)报告 平台 机制有差异 可 性。当使 Windows上 CITld工具时 个 尤其 注意。在 国 本 Windows 10中 命令 Shell使 是 旧 IBM437编码机制 它源 1982年IBM 个人 机。<sup>没</sup> 有任何官方 API提到 一点。Charset.defaultCharset( 方法将 回Windows-1252字 它 与IBM437完全不同。例如 在Windows-1252中有欧元 号€,但是在IBM437中没有。如果*

*System.out.printin("10 €");*

#### *控制台会显*

*iee ?*

*你可以建 户切换控制台 字 机制。在Windows中 可以通过chcp命令实 。例如*

*chcp 1252*

*会将控制台变换为Windows-1252 。*

*当然 想情况下你 户应 将控制台切换到UTF-8。在Windows中 命令为 chcp 65601*

*憾 是 命令 不 以 Java在控制台中使 UTF-8,我们 必 使 官方 file.encoding 属性来 平台 机制*

*java -Dfile.encoding=UTF-8 MyProg*

#### 7.6.4 日志文件

当来自 java.util.logging 库的日志消息被发送到控制台时,它们会用控制台的编码机制来书写。在上一节中你看到了如何进行控制。但是,文件中的日志消息会使用 FileHandler 来处理,它在默认情况下使用平台的编码机制。

要想将编码机制修改为 UTF-8, 需要修改日志管理器的设置。具体做法是在日志配置文件中做如下设置:

java.util.logging.FileHandler.encoding=UTF-8

#### 7.6.5 UTF-8 字节顺序标志

正如我们已经提到的,尽可能地让文本文件使用 UTF-8 是一个好的做法。如果你的应用必须读取其他程序创建的 UTF-8 文本文件,那么你可能会碰到另一个问题。在文件中添加一个"字节顺序标志"字符 U+FEFF 作为文件的第一个字符,是一种完全合法的做法。在UTF-16 编码机制中,每个码元都是一个两字节的数字,字节顺序标志可以告诉读入器该文件使用的是"高字节在前"还是"低字节在前"的字节顺序。UTF-8 是一种单字节编码机制,因此不需要指定字节的顺序。但是如果一个文件以字节 0xEF 0xBB 0xBF(U+FEFF的UTF-8 编码)开头,那么这就是一个强烈暗示,表示该文件使用了 UTF-8。正是这个原因,Unicode 标准鼓励这种实践方式。任何读入器都被认为会丢弃最前面的字节顺序标志。

还有一个瑕疵——Oracle 的 Java 实现很固执地因潜在的兼容性问题而拒绝遵循 Unicode 标准。作为程序员,这对你而言意味着必须去执行平台并不会执行的操作。在读入文本文件时,如果开头碰到了 U+FEFF,那就需要忽略它。

● 警告: 遗憾的是, JDK 的实现没有遵循这项建议。在向 javac 编译器传递有效的以字节顺序标志开头的 UTF-8 源文件时,编译会以产生错误消息 "illegal character: \65279"而失败。

#### 7.6.6 源文件的字符编码

作为程序员,要牢记你需要与 Java 编译器交互,这种交互需要通过本地系统的工具来完成。例如,可以使用中文版的记事本来写你的 Java 源代码文件。但这样写出来的源码不是随处可用的,因为它们使用的是本地的字符编码。只有编译后的 class 文件才能随处使用,因为它们会自动地使用"modified UTF-8"编码来处理标识符和字符串。这意味着即使在程序编译和运行时,也涉及 3 种字符编码:

- 源文件: 平台编码
- 类文件: modified UTF-8
- 虚拟机: UTF-16

关于 modified UTF-8 和 UTF-16 格式的定义,参见第 2 章。

☑ 提示: 可以用 -encoding 标记来设定源文件的字符编码, 例如: javac -encoding UTF-8 Myfile.java

#### 7.7 资源包

当本地化一个应用时,可能会有大量的消息字符串、按钮标签和其他的东西需要被翻译。 为了能灵活地完成这项任务,你肯定希望在外部定义消息字符串,这些消息字符串通常被称 为资源(resource)。这样,翻译人员不需要接触程序源代码就可以很容易地编辑资源文件。

在 Java 中,可以使用属性文件来设定字符串资源,并为其他类型的资源实现相应的类。

- 注释: Java 技术资源与 Windows 或 Macintosh 资源不同。Macintosh 或 Windows 可执行文件在程序代码以外的地方存储类似菜单、对话框、图标和消息这样的资源。资源编辑器能够在不影响程序代码的情况下检查并更新这些资源。
- i 注释: 卷 I 第 5 章描述了 JAR 文件资源的概念,以及为何数据文件、声音和图片可以存放在 JAR 文件中。Class 类的 getResource 方法可以找到相应的文件,打开它并返回资源的 URL。通过将文件放置到 JAR 文件中,将查找这些资源文件的工作留给了类的加载器去处理,加载器知道如何定位 JAR 文件中的项。但是,这种机制不支持 locale。

#### 7.7.1 定位资源包

当本地化一个应用时,会产生很多资源包(resource bundle)。每一个包都是一个属性文件或者是一个描述了与 locale 相关的项的类(比如消息、标签等)。对于每一个包,都要为所有你想要支持的 locale 提供相应的版本。

需要对这些包使用一种统一的命名规则。例如,为德国定义的资源放在一个名为 "baseName \_de\_DE"的文件中,而所有说德语的国家所共享的资源则放在名为 "baseName de"的文件中。一般来说,使用

baseName\_language\_country

来命名所有和国家相关的资源, 使用

baseName\_language

来命名所有和语言相关的资源。最后,作为后备,可以把默认资源放到一个没有后缀的文件中。

可以用下面的命令加载一个包:

ResourceBundle currentResources = ResourceBundle.getBundle(baseName, currentLocale);

getBundle 方法试图加载匹配当前 locale 定义的语言和国家的包。如果失败,通过依次放弃国家和语言来继续进行查找,然后同样的查找被应用于默认的 locale,最后,如果还不行

的话就去查看默认的包文件,如果这也失败了,则抛出一个 MissingResourceException 异常。 这就是说,getBundle 方法会试图加载以下包:

baseName\_currentLocaleLanguage\_currentLocaleCountry baseName\_currentLocaleLanguage baseName\_defaultLocaleLanguage\_defaultLocaleCountry baseName\_defaultLocaleLanguage baseName

一旦 getBundle 方法定位了一个包,比如,baseName\_de\_DE,它还会继续查找 baseName\_de 和 baseName 这两个包。如果这些包也存在,它们在资源层次中就成为 baseName\_de\_DE 的父包。以后,当查找一个资源时,如果在当前包中没有找到,就去查找其父包。就是说,如果一个特定的资源在当前包中没有找到,比如,某个特定资源在 baseName\_de\_DE 中没有找到,那么就会去查找 baseName de 和 baseName。

这是一项非常有用的服务,如果手工来编写将会非常麻烦。Java 编程语言的资源包机制会自动定位与给定的 locale 匹配得最好的项。可以很容易地把越来越多的本地化信息加到已有的程序中,你需要做的只是增加额外的资源包。

- 註釋: 我们简化了对资源包查找的讨论。如果 locale 中包含脚本或变体,那么查找就会复杂得多。可以查看 ResourceBundle.Control.getCandidateLocales 方法的文档以了解其细节。
- ▼ 提示: 不需要把你的程序的所有资源都放到同一个包中。可以用一个包来存放按钮标签,用另一个包存放错误消息等。

#### 7.7.2 属性文件

对字符串进行国际化是很直接的,可以把所有字符串放到一个属性文件中,比如 MyProgramStrings.properties,这是一个每行存放一个键 – 值对的文本文件。典型的属性文件看起来像下面这样:

computeButton=Rechnen
colorName=black
defaultPaperSize=210×297

然后像上一节描述的那样命名属性文件, 例如,

MyProgramStrings.properties
MyProgramStrings\_en.properties
MyProgramStrings\_de\_DE.properties

可以加载包,例如:

ResourceBundle bundle = ResourceBundle.getBundle("MyProgramStrings", locale);

要查找一个具体的字符串, 可以调用

String computeButtonLabel = bundle.getString("computeButton");

*告 在Java 9之前 存储属性 文件 是ASCII文件。如果你使 是旧 本 Java,并且需要将Unicode字 放到属性文件中 么 \uxxxx 方式对它们 行编码。比如 定"colorName=GrGn",可以使*

*colorName=Gr\u90FCn*

*你可以使 native2ascii工具来产生这些文件。*

#### *7.7.3<sup>包</sup>*

*为了提供字 串以外的资源 需要定义 它必 扩展 ResourceBundle 。应 使 标准 命名 则来命名你 比如*

```
MyProgramResources.java
MyProg ramResourcesen. j ava
MyProgramResources_de_DE•java
```

*可以使 与加 属性文件 同 getBundle方法来加 个*

*ResourceBundle bundle <sup>=</sup> Resou rceBundle.getBundle("MyProg ramResou rces", locale);*

*0 <sup>告</sup> 当搜 包时 如果 <sup>中</sup> 包和属性文件中 <sup>包</sup> 存在匹 则优先 <sup>择</sup> <sup>中</sup> <sup>包</sup>。*

*每一个 源包 实 了一个査 。你 为每一个你想定位 提供一个关 字 字 串 使 个字 串来提取 应 。例如*

```
var backgroundcolor = (Color) bundle.getObject("backgroundColor");
doubled paperSize = (doubled) bundle. getObj ect("defaultPaperSize");
```

*实 源包 最 单方法就是 承ListResourceBundle 。ListResourceBundle 你把所有 源 放到一个对 数 中并提供査找功 。 循以下 代 框架*

```
public class baseNameJanguage country extends ListResourceBundle
{
   private static final Object【】【】 contents =
   {
      { value2 }
      { key2i value2 },
   }
   public Object"【]getContentsO { return contents; }
}
例如
public class PrograraResourcesJe extends ListResourceBundle
{
   private static final Object[][] contents =
   {
      { 1backgroundcolor", Color.black },
      { BdefaultPaperSize"r new doublet] { 219, 297 } }
```

```
public Objects[] getContentsO { return contents; }
}
public class ProgramResources_en_US extends ListResourceBundle
{
   private static final Object[H】contents =
   {
      { "backgroundcolor**, Color.blue },
      { "defaultPaperSize", new doublet] { 216, 279 } }
   }
   public Object[][] getContentsO { return contents; }
}
```

*0 <sup>注</sup> 尺寸是以毫 为单位 <sup>出</sup> 。在世 <sup>上</sup> 了加拿大和 <sup>国</sup> 其他地区 <sup>使</sup> ISO <sup>216</sup> 格 。更多信息 http://www• cl• cam.ac• uk/-mgk25/iso-paper• html<sup>o</sup>*

*或 你的资源包 可以 承ResourceBundle 。然后 实 两个方法 一是枚举所 有 二是 定 査找 应 值*

```
Enumeration<String> getKeysf)
Object handleGetObject(String key)
```

*ResourceBundle类的getObject方法会 你提供 handleGetObj ect方法。*

#### *aw! java.util.ResourceBundle*

- *• static ResourceBundle getBundle(String baseName, Locale loc)*
- *• static ResourceBundle getBundle(String baseName) 在 定或 locale下以 定 名字加 源包 和它 。如果 源包 位于 一个Java包中 <sup>么</sup> 名字必 包含完整 包名 例如"inti. Prog ramResou rces<sup>M</sup> <sup>o</sup> 源包 必 是public 样getBundle方法才 它们。*
- *• Object getObject(String name) 从 源包或它 包中査找一个对 。*
- *• String getString(String name) 从 源包或它 包中査找一个对 并把它 型成字 串。*
- *• String!] getStringArray(String name) 从 源包或它的父包中査找一个对 并把它 型成字 串数 。*
- *• Enumeration<String> getKeys() 回一个枚举对 枚举出 源包中 所有 也包括 包中 。*
- *• Object handleGetObject(String key) 如果你 定义 己 源査找机制 么 个方法就 写 来査找与 定 关 源 值。*

#### *7.8 一个完整 例子*

*在 一 中 我们使 本 中 内容来对 休 器小 序 本地化 个小 序*

可以计算你是否为退休存够了钱。你需要输入年龄,每个月存多少钱等信息(参见图 7-4)。

![](_page_127_Figure_3.jpeg)

图 7-4 使用英语的退休金计算器

文本域和图表显示每年退休金账户中的余额。如果你后半生的退休金余额变成负数,并 且表中的数据条在 x 轴以下, 你就需要做些什么了。例如, 存更多的钱、推迟退休等。

这个退休金计算器可以在三种 locale (英语、德语和中文)下工作。下面是进行国际化时的一些要点:

- 标签、按钮和消息被翻译成德语和中文。你可以在 RetireResources\_de 和 RetireResources\_ zh 中找到它们。英语作为后备,见 RetireResources 文件。
- 当 locale 改变时,我们重置标签并格式化文本域中的内容。
- 文本域以本地格式处理数字、货币值和百分数。
- 计算域使用了 MessageFormat。格式字符串被存储在每种语言的资源包中。
- 为了展示该程序的确可行,我们按照用户选择的语言为条形图使用不同的颜色。

程序清单 7-4 到程序清单 7-7 展示了代码,而程序清单 7-8 到程序清单 7-10 是本地化的字符串的属性文件。图 7-5 和图 7-6 分别显示了在德语和中文下的输出。为了显示中文,请确认你已经在 Java 运行环境中安装并配置了中文字体,否则,所有的中文字符将会显示"missing character"图标。

#### 程序清单 7-4 retire/Retire.java

```
package retire;\nimport java.awt.*;\nimport java.awt.geom.*;\nimport java.text.*;\nimport java.util.*;
```

```
7
8
9
19
11
12
13
14
15
16
17
18
19
29
21
22
23
24
25
26
27
28
M
3
31
32
33
34
35
36
37
38
39
41
42
43
44
45
46
47
48
49
se
51
52
54
56
57
58
59
69
61
   import javax.swing.*;
    * This program shows a retirement calculator. The UI is displayed in English, German, and
    * Chinese.
    * (version 1.25 2018-65-91
    * ^author Cay Horstmann
    V
   public class Retire
   {
      public static void main(String[] args)
      {
         EventQueue.invokeLater(()->
             {
                var frame = new RetireFrameO;
                frame.setDefaultCloseOperation(JFrame.EXIT ON CLOSE);
                frame.setVisible(true);
             })
      }
   }
   class RetireFrame extends JFrarae
   {
      private JTextField savingsField = new JTextField(18);
      private JTextField contribField = new JTextField(16);
      private JTextField incomeField = new JTextField(18);
      private JTextField currentAgeField = new JTextField(4);
      private JTextField retireAgeField = new JTextField(4);
      private JTextField deathAgeField « new JTextField(4);
      private JTextField inflationPercentField = new JTextField(6);
      private JTextField investPercentField = new JTextField(6);
      private JTextArea retireText = new JTextArea(10, 25);
      private RetireComponent retireCanvas = new RetireComponent();
      private JButton conputeButton = new JButton();
      private JLabel languageLabel = new JLabelO
      private JLabel savingsLabel : new JLabel();
      private JLabel contribLabel = new JLabelO
      private JLabel incomeLabel = new JLabelO;
      private JLabel currentAgeLabel = new JLabel();
      private JLabel retireAgeLabel = new JLabeU)
      private JLabel deathAgeLabel = new JLabelO;
      private JLabel inflationPercentLabel = new JLabel();
       private JLabel investPercentLabel * new JLabelO;
       private Retireinfo info = new Retirelnfo();
       private Located locales = { Locale.US, Locale.CHINA, Locale.GERMANY };
       private Locale currentLocale;
       private JComboBox<Locale> localeCombo = new LocaleCombo(locales);
       private ResourceBundle res;
       private ResourceBundle resStrings;
       private NumberFormat currencyFmt;
       private NumberFormat numberFmt;
       private NumberFormat percentFrot;
       public RetireFrameO
```

```
add(inflationPercentField, new GBC(1, 3).setWeight(100, 0).setFill(GBC.HORIZONTAL));
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    add(investPercentField, new GBC(3, 3).setWeight(100, 0).setFill(GBC.HORIZONTAL));
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 add(currentAgeField, new GBC(1, 2).setWeight(100, 0).setFill(GBC.HORIZONTAL));
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     add(retireAgeField, new GBC(3, 2).setWeight(100, 0).setFill(GBC.HORIZONTAL));
add(deathAgeField, new GBC(5, 2).setWeight(100, 0).setFill(GBC.HORIZONTAL));
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      add(retireCanvas, new GBC(0, 4, 4, 1).setWeight(100, 100).setFill(GBC.BOTH));
                                                                                                                                                                                                                                                                                                                                                                                                              add(savingsField, new GBC(1, 1).setWeight(100, 0).setFill(GBC.HORIZONTAL));
add(contribField, new GBC(3, 1).setWeight(100, 0).setFill(GBC.HORIZONTAL));
add(incomeField, new GBC(5, 1).setWeight(100, 0).setFill(GBC.HORIZONTAL));
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              setCurrentLocale((Locale) localeCombo.getSelectedItem());
                                                                                                                                                                                                                                                                                               add(inflationPercentLabel, new GBC(0, 3).setAnchor(GBC.EAST));
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     new GBC(4, 4, 2, 1).setWeight(0, 100).setFill(GBC.BOTH));
                                                                                                                                                                                                                                                                                                                                            add(investPercentLabel, new GBC(2, 3).setAnchor(GBC.EAST));
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              retireText.setFont(new Font("Monospaced", Font.PLAIN, 10));
                                                                                                                                                                                     add(currentAgeLabel, new GBC(0, 2).setAnchor(GBC.EAST));
                                                                                                                                                                                                                         add(retireAgeLabel, new GBC(2, 2).setAnchor(GBC.EAST));
add(deathAgeLabel, new GBC(4, 2).setAnchor(GBC.EAST));
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  if (getLocale().equals(locales[i])) localeIndex = i;
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     int localeIndex = \theta; // US locale is default selection
setLayout(new GridBagLayout());
add(languageLabel, new GBC(0, 0).setAnchor(GBC.EAST));
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                // if current locale one of the choices, select it
                                                                          add(savingsLabel, new GBC(0, 1).setAnchor(GBC.EAST));
add(contribLabel, new GBC(2, 1).setAnchor(GBC.EAST));
                                                                                                                                              add(incomeLabel, new GBC(4, 1).setAnchor(GBC.EAST));
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        for (int i = 0; i < locales.length; i++)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    computeButton.addActionListener(event ->
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               setCurrentLocale(locales[localeIndex]);
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                computeButton.setName("computeButton");
                                                                                                                                                                                                                                                                                                                                                                            add(localeCombo, new GBC(1, 0, 3, 1));
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     localeCombo.addActionListener(event ->
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  add(computeButton, new GBC(5, 3));
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               info.setInflationPercent(0.05);
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 add(new JScrollPane(retireText)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              retireText.setEditable(false);
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         info.setInvestPercent(0.1);
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          info.setCurrentAge(35);
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 info.setContrib(9000);
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    info.setIncome(60000);
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              info.setRetireAge(65);
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       info.setDeathAge(85);
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       updateGraph();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               info.setSavings(0);
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     updateData();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    validate();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               getInfo();
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   105
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        901
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              187
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  1.08
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      189
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             110
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   11
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         113
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      116
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          88
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              101
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     192
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         103
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             184
                                                                                                                                                                                                                                                                                                                                                                                                                         74
                                                                                                                                                                                                                                                                                                                                                                                                                                                             12
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   16
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            00
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   82
```

```
});
117
         pack();
118
119
128
121
       * Sets the current locale.
122
       * @param locale the desired locale
123
124
      public void setCurrentLocale(Locale locale)
125
126
         currentLocale = locale:
127
         localeCombo.setLocale(currentLocale);
128
         localeCombo.setSelectedItem(currentLocale):
129
138
         res = ResourceBundle.getBundle("retire.RetireResources", currentLocale);
         resStrings = ResourceBundle.getBundle("retire.RetireStrings", currentLocale);
137
133
          currencyFmt = NumberFormat.getCurrencyInstance(currentLocale);
         numberFmt = NumberFormat.getNumberInstance(currentLocale);
134
         percentFmt = NumberFormat.getPercentInstance(currentLocale);
135
136
         updateDisplay();
137
         updateInfo();
138
139
         updateData();
         updateGraph();
148
141
142
143
       * Updates all labels in the display.
144
145
      public void updateDisplay()
146
147
          languageLabel.setText(resStrings.getString("language"));
148
          savingsLabel.setText(resStrings.getString("savings"));
7.40
          contribLabel.setText(resStrings.getString("contrib"));
156
          incomeLabel.setText(resStrings.getString("income"));
151
          currentAgeLabel.setText(resStrings.getString("currentAge"));
152
          retireAgeLabel.setText(resStrings.getString("retireAge"));
153
          deathAgeLabel.setText(resStrings.getString("deathAge"));
          inflationPercentLabel.setText(resStrings.getString("inflationPercent"));
155
          investPercentLabel.setText(resStrings.getString("investPercent"));
156
          computeButton.setText(resStrings.getString("computeButton"));
157
158
159
168
        * Updates the information in the text fields.
161
162
       public void updateInfo()
163
164
          savingsField.setText(currencyFmt.format(info.getSavings()));
165
          contribField.setText(currencyFmt.format(info.getContrib()));
166
          incomeField.setText(currencyFmt.format(info.getIncome()));
167
          currentAgeField.setText(numberFmt.format(info.getCurrentAge()));
168
          retireAgeField.setText(numberFmt.format(info.getRetireAge()));
169
          deathAgeField.setText(numberFmt.format(info.getDeathAge()));
178
          investPercentField.setText(percentFmt.format(info.getInvestPercent()));
```

```
inflationPercentField.setText(percentFmt.format(info.getInflationPercent()));
172
173
      }
174
      /**
175
       * Updates the data displayed in the text area.
176
177
      public void updateData()
178
      {
179
         retireText.setText("");
189
         var retireMsg = new MessageFormat("");
181
         retireMsg.setLocale(currentLocale);
182
          retireMsq.applyPattern(resStrings.getString("retire"));
183
184
         for (int i = info.getCurrentAge(); i <= info.getDeathAge(); i++)</pre>
185
186
             Object[] args = { i, info.getBalance(i) };
187
             retireText.append(retireMsg.format(args) + "\n");
188
         }
189
190
191
192
       * Updates the graph.
193
194
      public void updateGraph()
195
196
197
          retireCanvas.setColorPre((Color) res.getObject("colorPre"));
          retireCanvas.setColorGain((Color) res.getObject("colorGain"));
198
          retireCanvas.setColorLoss((Color) res.getObject("colorLoss"));
199
          retireCanvas.setInfo(info);
200
          repaint();
201
      }
202
203
284
       * Reads the user input from the text fields.
205
206
       public void getInfo()
207
208
          try
209
210
             info.setSavings(currencyFmt.parse(savingsField.getText()).doubleValue());
211
             info.setContrib(currencyFmt.parse(contribField.getText()).doubleValue());
212
             info.setIncome(currencyFmt.parse(incomeField.getText()).doubleValue());
213
214
             info.setCurrentAge(numberFmt.parse(currentAgeField.getText()).intValue());
             info.setRetireAge(numberFmt.parse(retireAgeField.getText()).intValue());
215
             info.setDeathAge(numberFmt.parse(deathAgeField.getText()).intValue());
216
             info.setInvestPercent(percentFmt.parse(investPercentField.getText()).doubleValue());
217
             info.setInflationPercent(
218
                percentFmt.parse(inflationPercentField.getText()).doubleValue());
219
          }
          catch (ParseException e)
221
          {
222
             e.printStackTrace();
223
224
225
226 }
```

```
227
228
229
23
231
232
233
234
235
236
237
238
239
246
241
242
243
244
245
246
247
248
249
256
251
252
253
2M
255
256
257
25S
259
266
261
262
2€3
264
265
266
267
268
2M
278
271
271
273
274
275
276
277
27B
279
289
281
    * The information required to compute retirement income data.
    */
   class Retireinfo
   {
       private double savings;
       private double contrib;
       private double income;
       private int currentAge;
       private int retireAge;
       private int deathAge;
       private double inflationPercent;
       private double investPercent;
       private int age;
       private double balance;
        * Gets the available balance for a given year.
        * param year the year for which to compute the balance
        * @return the amount of money available (or required) in that year
        7
       public double getBalance(int year)
       {
          if (year < currentAge) return
          else if (year « currentAge)
          {
              age = year;
              balance = savings;
              return balance;
          }
          else if (year = age) return balance;
          if (year != age + 1) getBalance(year - 1);
          age = year;
          if (age < retireAge) balance += contrib;
          else balance •= income;
          balance = balance * (1 + (investPercent • inflationPercent));
          return balance;
       }
        * Gets the amount of prior savings.
        * ^return the savings amount
       public double getSavingsO
       {
           return savings;
       }
       /
        * Sets the amount of prior savings.
        * 卽a ram newValue the savings amount
          /
       public void setSavings(double newValue)
```

```
282
283
284
285
286
287
288
289
294
291
292
293
294
295
296
297
298
299
3
361
382
383
3G4
3G5
3
397
308
399
316
312
313
314
316
317
318
319
320
321
322
323
324
325
326
327
328
329
338
331
332
334
336
          savings = newValue;
       }
       /**
          Gets the annual contribution to the retirement account.
          ^return the contribution amount
          /
       public double getContribO
       {
           return contrib;
       }
       /**
        * Sets the annual contribution to the retirement account.
        * @param newValue the contribution amount
        */
       public void setContrib(double newValue)
       {
           contrib = newValue;
       }
       /**
        * Gets the annual income.
        * ©return the income amount
        */
       public double getlncome()
       {
           return income;
       }
       /*
           Sets the annual income.
           @param newValue the income aiiK)unt
          /
       public void setlncomefdouble newValue)
       {
           income = newValue;
       }
       /**
        * Gets the current age.
        * @return the age
        */
       public int getCurrentAgeO
       {
           return currentAge;
       }
       /»»
           Sets the current age.
           @parain newValue the age
          /
       public void setCurrentAge(int newValue)
           currentAge = newValue
```

```
}
337
338
      /**
339
       * Gets the desired retirement age.
340
       * @return the age
341
342
      public int getRetireAge()
343
344
          return retireAge;
345
      }
346
347
348
       * Sets the desired retirement age.
349
        * @param newValue the age
350
351
      public void setRetireAge(int newValue)
352
353
          retireAge = newValue;
354
      }
355
356
357
        * Gets the expected age of death.
358
        * @return the age
359
36B
       public int getDeathAge()
361
362
          return deathAge;
363
364
365
366
        * Sets the expected age of death.
367
        * @param newValue the age
368
369
       public void setDeathAge(int newValue)
370
371
          deathAge = newValue;
372
373
374
375
        * Gets the estimated percentage of inflation.
376
        * @return the percentage
377
378
       public double getInflationPercent()
379
388
          return inflationPercent;
381
382
383
       /**
384
        * Sets the estimated percentage of inflation.
385
        * @param newValue the percentage
386
387
       public void setInflationPercent(double newValue)
388
389
          inflationPercent = newValue;
398
       }
391
```

```
392
393 /**
394 Gets theestimated yield of the investment.
395 * ^returnthepercentage
396 /
397 public double getlnvestPercentO
398 {
399 return investPercent;
     }
<ei
462 /*
<63 * Sets the estimated yield of the investment.
484 @param newValue the percentage
<es /
48« public void setinvestPercent(double newValue)
487 {
488 investPercent = newValue;
499 }
4ie }
411
412 /
413 This component draws a graph of the investment result.
414/
415 class RetireComponent extends JComponent
416 {
417 private static final int PANEL WIDTH = 400;
418 private static final int PANEL HEIGHT = 206;
419 private static final Dimension PREFERRED SIZE = new Dimension(800, 600);
42e private Retireinfo info = null;
421 private Color colorPre;
422 private Color colorGain;
<23 private Color colorLoss;
424
425 public RetireComponent()
426 {
427 setSize(PANEL_WIDTH, PANEL HEIGHT);
428 }
429
436 /
431 * Setstheretirement information to be plotted.
432 @paramnewlnfo the newretirement info.
433 /
434 public void setInfo(RetireInfo newlnfo)
435 {
436 info = newlnfo;
437 repaint();
438 }
439
440public void paintComponent(Graphics g)
441 {
442 var g2 = (Graphics2D) g;
443if (info == null) return;
444
445 double minValue =
446 double maxValue = 8;
```

```
int i;
447
          for (i = info.getCurrentAge(); i <= info.getDeathAge(); i++)</pre>
448
449
             double v = info.getBalance(i);
450
             if (minValue > v) minValue = v;
451
             if (maxValue < v) maxValue = v;
452
453
          if (maxValue == minValue) return;
454
455
          int barWidth = getWidth() / (info.getDeathAge() - info.getCurrentAge() + 1);
456
          double scale = getHeight() / (maxValue - minValue);
457
458
          for (i = info.getCurrentAge(); i <= info.getDeathAge(); i++)</pre>
459
468
             int x1 = (i - info.getCurrentAge()) * barWidth + 1;
461
462
             double v = info.getBalance(i);
463
             int height;
464
             int yOrigin = (int) (maxValue * scale);
466
             if (v >= 0)
457
468
                y1 = (int) ((maxValue - v) * scale);
469
                height = y0rigin - y1;
479
             }
471
             else
472
473
                y1 = y0rigin;
474
                 height = (int) (-v * scale);
475
476
477
             if (i < info.getRetireAge()) g2.setPaint(colorPre);</pre>
478
             else if (v \ge 0) q2.setPaint(colorGain);
479
             else g2.setPaint(colorLoss);
480
             var bar = new Rectangle2D.Double(x1, y1, barWidth - 2, height);
481
              q2.fill(bar);
482
             g2.setPaint(Color.black);
483
             g2.draw(bar);
484
485
       }
486
487
       /**
488
        * Sets the color to be used before retirement.
489
        * @param color the desired color
498
 491
       public void setColorPre(Color color)
 492
493
          colorPre = color;
 494
          repaint();
 495
       }
 496
 497
       /**
 498
        * Sets the color to be used after retirement while the account balance is positive.
 499
        * @param color the desired color
 500
 581
```

```
public void setColorGain(Color color)
502
      {
503
          colorGain = color;
504
          repaint();
505
      }
586
507
508
       * Sets the color to be used after retirement when the account balance is negative.
500
       * @param color the desired color
510
511
      public void setColorLoss(Color color)
512
513
          colorLoss = color;
514
          repaint();
515
516
517
      public Dimension getPreferredSize() { return PREFERRED SIZE; }
518
519 }
```

#### 程序清单 7-5 retire/RetireResources.java

```
1 package retire;
2
3 import java.awt.*;
4
5 /**
   * These are the English non-string resources for the retirement calculator.
   * @version 1.21 2001-08-27
   * @author Cay Horstmann
   */
9
10
   public class RetireResources extends java.util.ListResourceBundle
11
      private static final Object[][] contents =
12
13
14
         // BEGIN LOCALIZE
         { "colorPre", Color.blue }, { "colorGain", Color.white }, { "colorLoss", Color.red }
15
         // END LOCALIZE
16
      }:
17
18
      public Object[][] getContents()
19
20
         return contents;
21
22
23 }
```

#### 程序清单 7-6 retire/RetireResources\_de.java

```
package retire;
\nimport java.awt.*;

/**

* These are the German non-string resources for the retirement calculator.

* @version 1.21 2001-08-27
```

```
* @author Cay Horstmann
   */
9
  public class RetireResources de extends java.util.ListResourceBundle
10
11
      private static final Object[][] contents =
12
13
         // BEGIN LOCALIZE
14
         { "colorPre", Color.yellow }, { "colorGain", Color.black }, { "colorLoss", Color.red }
15
         // END LOCALIZE
16
17
      };
18
      public Object[][] getContents()
19
28
         return contents;
21
22
      }
   }
23
```

#### 程序清单 7-7 retire/RetireResources\_zh.java

```
1 package retire;
2
  import java.awt.*;
4
5 /**
    * These are the Chinese non-string resources for the retirement calculator.
    * @version 1.21 2001-08-27
    * @author Cay Horstmann
8
9
   public class RetireResources zh extends java.util.ListResourceBundle
10
   {
11
      private static final Object[][] contents =
12
13
         // BEGIN LOCALIZE
14
         { "colorPre", Color.red }, { "colorGain", Color.blue }, { "colorLoss", Color.yellow }
15
         // END LOCALIZE
16
      };
17
18
      public Object[][] getContents()
19
20
         return contents;
21
      }
22
23 }
```

#### 程序清单 7-8 retire/RetireStrings.properties

language=Language
computeButton=Compute
savings=Prior Savings
contrib=Annual Contribution\nincome=Retirement Income
currentAge=Current Age
retireAge=Retirement Age
deathAge=Life Expectancy\ninflationPercent=Inflation

- *ie investPercent=Investment Return*
- *li retire=Age: {0,number} Balance: {1,number,currency}*

#### *序清单 7-9 retire/RetireStrings\_de.properties*

- *language=Sprache*
- *computeButton=Rechnen*
- *savings=Vorherige Ersparnisse*
- *contrib=Jahrliche Einzahlung*
- *incorae=Einkoiwnen nach Ruhestand*
- *currentAge=Jetziges Alter*
- *? retireAge=Ruhestandsalter*
- *deathAge<ebenserwartung*
- *inflationPercent=Inflation*
- *ie investPercent=Investitionsgewinn*
- *u retire=Alter: {0,number} Guthaben: {1,number,currency}*

#### *序清单 7-10 retire/RetireStrings\_zh.properties*

- *language:;吾宮*
- *computeButton=*
- *savings\*tt<sup>存</sup>*
- *contrib=每年存*
- *incomes 休收入*
- *currentAge=现龄*
- *retireAge=il休年*
- *deathAges 期寿命*
- *inflationPercent=*
- *ie investPercent®投 报*
- *li retire\*<sup>年</sup> {0,number}<sup>总</sup> {1,number,currency}*

![](_page_139_Figure_27.jpeg)

*图7-5<sup>使</sup> <sup>德</sup> <sup>休</sup> <sup>器</sup>*

![](_page_140_Figure_1.jpeg)

图 7-6 使用中文的退休金计算器

本章进述了如何运用 Java 语言的国际化特性。现在你可以使用资源包来提供多种语言的转换,也可以使用格式器和排序器来处理与 locale 相关的文本了。

下一章将研究脚本编写、编译和注解处理。

## *8 本、编译与注 <sup>处</sup>*

- *Java平台 本机制*
- *▲ 器API*
- *▲使 注*
- *▲<sup>注</sup> <sup>法</sup>*

- *▲标准注*
- *▲源 注 处*
- *▲字节码工*

*本 将介 三 于处 代 技术 本API使你可以 如JavaScript和Groovy 样 本 代 当你希望在应 序内 Java代 时 可以使 器API 注 处 器可以在包含注 Java源代 和 文件上 操作。如你所 有 多应 序 可以 来处 注 从 单 断到"字节码工 " 后 可以将字 插入到 文件中 甚至可以插入到正在运行的程序中。*

#### *8.1 Java平台 本机制*

*本 是一 在 时 序文本 从 免使 常 / / 接/ 循 。 本 有 多优势*

- *便于快 变更 励不断 。*
- *可以修改 序 为。*
- *支持 序 户 定制化。*

*另外 大多数 本 乏可以使 写复杂应 受 性 例如强 型、封 和模 块化。*

*因此人们在尝 将 本 和传 优势 合。 本API使你可以在Java平台上 实 个 它支持在Java 序中对 JavaScript、Groovy、Ruby, 是更奇异 如 Scheme和Haskell 写 本 。例如 Rer^jin项目(www.renjin.org)就提供了一 个R编程语言的Java实 和 应 本API "引擎" R语言被广泛应 于统计编程中。*

*在下 小 中 我们将向你展 如何为某 定 择一个引擎 如何执行脚 本 以及如何利 某些 本引擎提供 先 性。*

#### *8.1.1 <sup>取</sup> 本引擎*

*本引擎是一个可以执 某 定 写 本 库。当 拟机启动时 它 会发 可 本引擎。为了枚举 些引擎 构 一个ScriptEngineManager,并 getEngineFactories方法。可以向每个引擎工厂 它们所支持 引擎名、MIME 型和文件* 扩展名。表 8-1 显示了这些内容的典型值。

| 引擎                | 名 字                                  | MIME 类型                                                                                       | 文件扩展       |
|-------------------|--------------------------------------|-----------------------------------------------------------------------------------------------|------------|
| Rhino(JavaScript) | rhino, Rhino, JavaScript, javascript | <pre>application/javascript, application/\necmascript, text/javascript, text/ecmascript</pre> | js         |
| Groovy            | groovy                               | 无                                                                                             | groovy     |
| Renjin            | Renjin                               | text/x-R                                                                                      | R, r, S, s |

表 8-1 脚本引擎工厂的属性

通常,你知道所需要的引擎,因此可以直接通过名字、MIME类型或文件扩展来请求它,例如:

var manager = new ScriptEngineManager();

ScriptEngine engine = manager.getEngineByName("javascript");

可以通过在类路径中提供必要的 JAR 文件来添加对更多语言的支持。oracle JDK 中以往都包含一个 JavaScript 引擎,但是在 Java 15 中被移除了。

#### API javax.script.ScriptEngineManager

- List<ScriptEngineFactory> getEngineFactories()
   获取所有发现的引擎工厂的列表。
- ScriptEngine getEngineByName(String name)
- ScriptEngine getEngineByExtension(String extension)
- ScriptEngine getEngineByMimeType(String mimeType)
   获取给定名字、脚本文件扩展名或 MIME 类型的脚本引擎。

#### API javax.script.ScriptEngineFactory 6

- List<String> getNames()
- List<String> getExtensions()
- List<String> getMimeTypes()

获取该工厂所了解的名字、脚本文件扩展名和 MIME 类型。

#### 8.1.2 脚本计算与绑定

一旦拥有了引擎,就可以通过下面的调用来直接调用脚本:

Object result = engine.eval(scriptString);

如果脚本存储在文件中,那么需要先打开一个 Reader,然后调用:

Object result = engine.eval(reader);

可以在同一个引擎上调用多个脚本。如果一个脚本定义了变量、函数或类,那么大多数引擎都会保留这些定义,以供将来使用。例如:

engine.eval("n = 1728");
Object result = engine.eval("n + 1");

将返回 1729。

註釋: 要想知道在多个线程中并发执行脚本是否安全, 可以调用

Object param = factory.getParameter("THREADING");

其返回的是下列值之一:

- null: 并发执行不安全。
- "MULTITHREADED": 并发执行安全。一个线程的执行效果对另外的线程有可能是可视的。
- "THREAD-ISOLATED": 除了 "MULTITHREADED", 还会为每个线程维护不同的变量绑定。
- "STATELESS": 除了 "THREAD-ISOLATED", 脚本还不会改变变量绑定。

我们经常希望能够向引擎中添加新的变量绑定。绑定由名字及其关联的 Java 对象构成。例如,考虑下面的语句:

```
engine.put("k", 1728);
Object result = engine.eval("k + 1");
```

脚本代码从"引擎作用域"中的绑定里读取 k 的定义。这一点非常重要,因为大多数脚本语言都可以访问 Java 对象,通常使用的是比 Java 语法更简单的语法。例如,

```
engine.put("b", new JButton());\nengine.eval("b.text = '0k'");
```

反过来,也可以获取由脚本语句绑定的变量:

```
engine.eval("n = 1728");
Object result = engine.get("n");
```

除了引擎作用域之外,还有全局作用域。任何添加到 ScriptEngineManager 中的绑定对所有引擎都是可视的。

除了向引擎或全局作用域添加绑定之外,还可以将绑定收集到一个类型为 Bindings 的对象中,然后将其传递给 eval 方法:

```
Bindings scope = engine.createBindings();
scope.put("b", new JButton());\nengine.eval(scriptString, scope);
```

如果绑定集不应该为了将来对 eval 方法的调用而持久化,那么这么做就很有用。

這一注釋:你可能希望除了引擎作用域和全局作用域之外还有其他的作用域。例如,Web容器可能需要请求作用域或会话作用域。但是,这需要你自己去解决。你需要实现一个类,它实现了 ScriptContext 接口,并管理着一个作用域集合。每个作用域都是由一个整数标识的,而且越小的数字应该越先被搜索。(标准类库提供了 SimpleScriptContext 类,但是它只能持有全局作用域和引擎作用域。)

#### API javax.script.ScriptEngine 6

- Object eval(String script)
- Object eval(Reader reader)
- Object eval(String script, Bindings bindings)

- Object eval(Reader reader, Bindings bindings)
   对由字符串或读取器给定的脚本进行计算,并服从给定的绑定。
- Object get(String key)
- void put(String key, Object value)
   在引擎作用域内获取或放置一个绑定。
- Bindings createBindings()
   创建一个适合该引擎的空 Bindings 对象。

#### api javax.script.ScriptEngineManager

- Object get(String key)
- void put(String key, Object value)
   在全局作用域内获取或放置一个绑定。

#### API javax.script.Bindings 6

- Object get(String key)
- void put(String key, Object value)
   在由该 Bindings 对象表示的作用域内获取或放置一个绑定。

#### 8.1.3 重定向输入和输出

可以通过调用脚本上下文的 setReader 和 setWriter 方法来重定向脚本的标准输入和输出。例如,

```
var writer = new StringWriter();\nengine.getContext().setWriter(new PrintWriter(writer, true));
```

在上例中,任何用 JavaScript 的 print 和 println 函数产生的输出都会被发送到 writer。 setReader 和 setWriter 方法只会影响脚本引擎的标准输入和输出源。例如,如果执行下面 的 JavaScript 代码:

```
println("Hello");
java.lang.System.out.println("World");
```

则只有第一个输出会被重定向。

Rhino 引擎没有标准输入源的概念,因此调用 setReader 没有任何效果。

#### API javax.script.ScriptEngine 6

ScriptContext getContext()
 获得该引擎的默认的脚本上下文。

#### API javax.script.ScriptContext

- Reader getReader()
- void setReader(Reader reader)

- Writer getWriter()
- void setWriter(Writer writer)
- Writer getErrorWriter()
- void setErrorWriter(Writer writer)

获取或设置用于输入的读入器或用于正常与错误输出的写出器。

#### 8.1.4 调用脚本的函数和方法

对于许多脚本引擎而言,我们都可以调用脚本语言的函数,而不必对实际的脚本代码进行计算。如果允许用户用他们所选择的脚本语言来实现服务,那么这种机制就很有用了。

提供这种功能的脚本引擎实现了 Invocable 接口。特别是, Rhino 引擎就是实现了 Invocable 接口。

要调用一个函数,需要用函数名来调用 invokeFunction 方法,函数名后面是函数的参数:

```
// Define greet function in JavaScript\nengine.eval("function greet(how, whom) { return how + ', ' + whom + '!' }");

// Call the function with arguments "Hello", "World"
result = ((Invocable) engine).invokeFunction("greet", "Hello", "World");

如果脚本语言是面向对象的,那就可以调用 invokeMethod:

// Define Greeter class in JavaScript\nengine.eval("function Greeter(how) { this.how = how }");\nengine.eval("Greeter.prototype.welcome = "
```

- **注释**: Rhino 不支持当今的 JavaScript 的类语法,关于如何用 JavaScript 老式的语法定义类的更多细节,可以参阅 *JavaScript: The Good Parts*, Douglas Grockford 著(O'Reilly, 2008)。
- **注释**:即使脚本引擎没有实现 Invocable 接口, 你也可能仍旧可以以一种独立于语言的方式来调用某个方法。ScriptEngineFactory 类的 getMethodCallSyntax 方法可以产生一个字符串, 你可以将其传递给 eval 方法。但是, 在这样调用时, 所有的方法参数必须都与名字绑定, 而 invokeMethod 方法是可以用任意值调用的。

我们可以更进一步,让脚本引擎去实现一个 Java 接口,然后就可以用 Java 方法调用的语法来调用脚本函数。

其细节依赖于脚本引擎,但是典型情况是我们需要为该接口中的每个方法都提供一个函数。例如,考虑下面的 Java 接口:

```
public interface Greeter
{
    String welcome(String whom);
}
如果用 Rhino 定义了具有相同名字的函数,那么可以通过这个接口来调用它:
// Define welcome function in JavaScript\nengine.eval("function welcome(whom) { return 'Hello, ' + whom + '!' }");
// Get a Java object and call a Java method
Greeter g = ((Invocable) engine).getInterface(Greeter.class);
result = g.welcome("World");
```

在面向对象的脚本语言中,可以通过相匹配的 Java 接口来访问一个脚本类。例如,下面的代码展示了如何使用 Java 的语法来调用 JavaScript 的 SimpleGreeter 类:

```
Greeter g = ((Invocable) engine).getInterface(yo, Greeter.class);
result = g.welcome("World");
```

总之,如果你希望从 Java 中调用脚本代码,同时又不想因这种脚本语言的语法而受到困扰,那么 Invocable 接口就很有用。

#### API javax.script.Invocable 6

- Object invokeFunction(String name, Object... parameters)
- Object invokeMethod(Object implicitParameter, String name, Object... explicitParameters) 用给定的名字调用函数或方法,并传递给定的参数。
- <T> T getInterface(Class<T> iface) 返回给定接口的实现,该实现用脚本引擎中的函数实现了接口中的方法。
- <T> T getInterface(Object implicitParameter, Class<T> iface)
   返回给定接口的实现、该实现用给定对象的方法实现了接口中的方法。

#### 8.1.5 编译脚本

某些脚本引擎出于对执行效率的考虑,可以将脚本代码编译为某种中间格式。这些引擎 实现了 Compilable 接口。下面的示例展示了如何编译和计算包含在脚本文件中的代码:

```
var reader = new FileReader("myscript.js");
CompiledScript script = null;\nif (engine implements Compilable)
    script = ((Compilable) engine).compile(reader);
```

一旦该脚本被编译,就可以执行它。下面的代码将会在编译成功的情况下执行编译后的脚本,如果引擎不支持编译,则执行原始的脚本。

```
if (script != null)
    script.eval();\nelse
    engine.eval(reader);
```

当然,只有需要重复执行时,我们才希望编译脚本。

#### API javax.script.Compilable 6

- CompiledScript compile(String script)
- CompiledScript compile(Reader reader)
   编译由字符串或读入器给定的脚本。

#### API javax.script.CompiledScript

- Object eval()
- Object eval(Bindings bindings)
   对该脚本计算。

#### 8.1.6 示例: 用脚本处理 GUI 事件

为了演示脚本 API, 我们将开发一个样例程序, 它允许用户指定使用他们所选择的脚本语言编写的事件处理器。

让我们看看程序清单 8-1 中的程序,它可以将脚本添加到任意的框体类中。默认情况下,它会读取程序清单 8-2 中的 ButtonFrame 类, ButtonFrame 类与卷 I 中介绍的事件处理演示程序类似,但是有两个差异:

- 每个构件都有其自己的 name 属性集。
- 没有任何事件处理器。

事件处理器是在属性文件中定义的。每个属性定义都具有下面的形式:

componentName.eventName = scriptCode

例如,如果选择使用 JavaScript,那就要在 js.properties 文件中提供事件处理器:

yellowButton.action=panel.background = java.awt.Color.YELLOW blueButton.action=panel.background = java.awt.Color.BLUE redButton.action=panel.background = java.awt.Color.RED

本书附带的代码还包括用于 Groovy 和 R 的文件。

该程序以加载在命令行中指定的语言所需的引擎开始,如果未指定语言,则使用 JavaScript。然后,我们处理init.language 脚本,如果该文件存在的话。这对像 R 语言这样的语言很有用,因为这些语言需要某些麻烦的初始化工作,我们不希望在每个事件处理器的脚本中都包括这部分工作。

接下来,我们递归地遍历所有的子构件,并在构件映射表中添加(名字,对象)绑定,然后,将它们添加到引擎中。

然后,我们读入 language.properties 文件。对于每一个属性,都合成其事件处理器代理,使得脚本代码得以执行。其细节有些技术性,如果你希望了解实现的细节,请参阅卷 I 第 6 章有关代理的小节。但是,其精髓部分是每个事件处理器都会调用下面的方法:

engine.eval(scriptCode);

让我们详细看看 yellowButton。当下面一行被处理时,

yellowButton.action=panel.background = java.awt.Color.YELLOW

我们找到了具有"yellowButton"名字的 JButton 构件,然后附着一个 ActionListener,它拥有 actionPerformed 方法,该方法将执行下面的脚本,如果该脚本是用 Rhino 执行的:

panel.background = java.awt.Color.YELLOW

引擎包含一个将名字"panel"与这个 JPanel 对象绑定在一起的绑定。当事件发生时,该面板的 setBackground 方法就会执行,并且其颜色也会改变。

如果使用的是 Java 15 或以上的版本,那么类路径中必须包含一个像 Rhino 这样的 JavaScript 引擎 (https://github.com/mozilla/rhino)。应该像下面这样运行该程序:

java -classpath .:rhino-version.jar:rhino-engine-version.jar ScriptTest

对于 Groovy 处理器,需要使用

java -classpath .:groovy/lib/\\* ScriptTest groovy

这里, groovy 是 Groovy 的安装目录。

对于R的Renjin 实现,要在类路径中包含Renjin Studio的JAR文件以及Renjin 脚本引擎。它们都可以在www.renjin.org/downloads.html 处获得。

这个应用演示了如何在 Java GUI 编程中使用脚本机制。大家可以更进一步,用 XML 文件来描述 GUI,就像在第 3 章中看到的那样。然后我们的程序就会变成解释器,去解释那些由 XML 文件定义可视化表示以及用脚本语言定义行为的 GUI。请注意这与动态 HTML 页面或动态服务器端脚本环境之间的相似性。

#### 程序清单 8-1 script/ScriptTest.java

```
package script;
2
3 import java.awt.*;
4 import java.beans.*;
5 import java.io.*;
 6 import java.lang.reflect.*;
7 import java.nio.charset.*;
8 import java.util.*;
9 import javax.script.*;
10 import javax.swing.*;
11
12 /**
   * @version 1.04 2021-06-17
13
   * @author Cay Horstmann
14
15
16 public class ScriptTest
17
      public static void main(String[] args)
18
19
         EventOueue.invokeLater(() ->
28
21
               try
22
23
                   var manager = new ScriptEngineManager();
24
```

```
String language;
25
                   if (args.length == 0)
26
27
                      System.out.println("Available factories: ");
28
                      for (ScriptEngineFactory factory : manager.getEngineFactories())
29
                         System.out.println(factory.getEngineName());
30
31
                      language = "nashorn";
32
                   }
33
                   else language = args[\theta];
34
35
                   final ScriptEngine engine = manager.getEngineByName(language);
36
                   if (engine == null)
37
                   {
38
                      System.err.println("No engine for " + language);
39
                      System.exit(1);
40
                   }
41
42
                   final String frameClassName
43
                      = args.length < 2 ? "buttons1.ButtonFrame" : args[1];</pre>
45
                   var frame
46
                      = (JFrame) Class.forName(frameClassName).getConstructor().newInstance();
47
                   InputStream in = frame.getClass().getResourceAsStream("init." + language);
48
                   if (in != null) engine.eval(
49
                       new InputStreamReader(in, StandardCharsets.UTF 8));
                   var components = new HashMap<String, Component>();
51
                   getComponentBindings(frame, components);
52
                   components.forEach((name, c) -> engine.put(name, c));
53
54
                   var events = new Properties();
55
                   in = frame.getClass().getResourceAsStream(language + ".properties");
                   events.load(
57
                       new InputStreamReader(in, StandardCharsets.UTF 8));
58
59
                   for (Object e : events.keySet())
68
61
                       String[] s = ((String) e).split("\\.");
62
                       addListener(s[0], s[1], (String) events.get(e), engine, components);
63
                   frame.setTitle("ScriptTest");
65
                   frame.setDefaultCloseOperation(JFrame.EXIT ON CLOSE);
66
                    frame.setVisible(true);
68
                catch (ReflectiveOperationException | IOException
69
                       | ScriptException | IntrospectionException e)
                {
71
                    e.printStackTrace();
72
                }
             });
74
75
76
77
        * Gathers all named components in a container.
78
        * @param c the component
79
```

```
* @param namedComponents a map into which to enter the component names and components
80
       */
81
      private static void getComponentBindings(Component c,
82
            Map<String, Component> namedComponents)
83
84
         String name = c.getName();
85
         if (name != null) { namedComponents.put(name, c); }
86
         if (c instanceof Container container)
87
         {
88
            for (Component child : container.getComponents())
89
               getComponentBindings(child, namedComponents);
90
91
92
93
      /**
94
       * Adds a listener to an object whose listener method executes a script.
95
       * @param beanName the name of the bean to which the listener should be added
96
       * @param eventName the name of the listener type, such as "action" or "change"
97
       * @param scriptCode the script code to be executed
98
       * Oparam engine the engine that executes the code
99
       * Oparam bindings the bindings for the execution
100
       * @throws IntrospectionException
101
102
      private static void addListener(String beanName, String eventName, final String scriptCode,
103
            ScriptEngine engine, Map<String, Component> components)
104
            throws ReflectiveOperationException, IntrospectionException
165
186
         Object bean = components.get(beanName);
107
         EventSetDescriptor descriptor = getEventSetDescriptor(bean, eventName);
198
         if (descriptor == null) return;
109
         descriptor.getAddListenerMethod().invoke(bean,
118
             Proxy.newProxyInstance(null, new Class[] { descriptor.getListenerType() },
111
                (proxy, method, args) ->
112
113
                      engine.eval(scriptCode);
114
                      return null;
115
                   }));
116
117
118
      private static EventSetDescriptor getEventSetDescriptor(Object bean, String eventName)
119
             throws IntrospectionException
128
121
          for (EventSetDescriptor descriptor : Introspector.getBeanInfo(bean.getClass())
122
                .getEventSetDescriptors())
             if (descriptor.getName().equals(eventName)) return descriptor;
174
          return null;
125
      }
126
127 }
```

#### 程序清单 8-2 buttons1/ButtonFrame.java

```
package buttons1;\nimport javax.swing.*;
```

```
4
5
    * A frame with a button panel.
    * @version 1.00 2007-11-02
    * @author Cay Horstmann
9
   public class ButtonFrame extends JFrame
10
11
      private static final int DEFAULT WIDTH = 300;
12
      private static final int DEFAULT_HEIGHT = 200;
13
14
      private JPanel panel;
15
      private JButton vellowButton;
16
      private JButton blueButton;
17
      private JButton redButton;
18
19
      public ButtonFrame()
20
      {
21
         setSize(DEFAULT WIDTH, DEFAULT HEIGHT);
22
23
         panel = new JPanel();
24
         panel.setName("panel");
25
         add(panel);
26
27
         yellowButton = new JButton("Yellow");
28
         yellowButton.setName("yellowButton");
29
          blueButton = new JButton("Blue");
38
          blueButton.setName("blueButton");
31
          redButton = new JButton("Red"):-
32
          redButton.setName("redButton");
33
34
          panel.add(yellowButton);
35
          panel.add(blueButton);
36
          panel.add(redButton);
37
38
  }
39
```

#### 8.2 编译器 API

有许多工具都需要编译 Java 代码。很明显,教授 Java 编程的开发环境和程序就位于其列,测试和自动化构建工具也属于这类工具。另一个例子是 JavaServer Pages 的处理工具, JSP 是一种嵌入了 Java 语句的网页。

#### 8.2.1 调用编译器

调用编译器非常简单,下面是一个示范调用:

```
JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
OutputStream outStream = . . .;
OutputStream errStream = . . .;\nint result = compiler.run(null, outStream, errStream,
    "-sourcepath", "src", "Test.java");
```

返回值为 0表示编译成功。

编译器会向提供给它的流发送输出和错误消息。如果将这些参数设置为 null,编译器就会使用 System.out 和 System.err。run 方法的第一个参数是输入流,由于编译器不会接受任何控制台输入,因此总是应该让其保持为 null。(run 方法是从泛化的 Tool 接口继承而来的,它考虑到某些工具需要读取输入。)

如果在命令行调用 javac, 那么 run 方法其余的参数就会作为变量传递给 javac。这些变量是一些选项或文件名。

#### 8.2.2 发起编译任务

可以通过使用 CompilationTask 对象来对编译过程进行更多的控制。如果要从字符串中提供源码,在内存中捕获类文件,或者处理错误和警告消息,这样做就会显得很有用。

要想获取 CompilationTask 对象,需要以前一节中描述的 compiler 对象开始,然后按照下面的方式调用:

```
JavaCompiler.CompilationTask task = compiler.getTask(
  errorWriter, // Uses System.err if null
  fileManager, // Uses the standard file manager if null
  diagnostics, // Uses System.err if null
  options, // null if no options
  classes, // For annotation processing; null if none
  sources);
```

最后三个参数是 Iterable 的实例。例如,选项序列可以像下面这样指定:

Iterable<String> options = List.of("-d", "bin");

sources 参数是 JavaFileObject 实例的 Iterable。如果想要编译磁盘文件,需要获取一个 StandardJavaFileManager 对象,并调用其 getJavaFileObjects 方法:

```
StandardJavaFileManager fileManager = compiler.getStandardFileManager(null, null);
Iterable<JavaFileObject> sources
```

**注释:** classes 参数只用于注解处理。在这种情况下,还需要用一个 Processor 对象的列表来调用 task.processors(annotationProcessors)。请参见 8.6 节中有关注解处理的示例。

getTask方法会返回任务对象,但是并不会启动编译过程。CompilationTask类扩展了Callable<Boolean>, 我们可以将其对象传递给ExecutorService以并行执行,或者只是做出如下的同步调用:

Boolean success = task.call();

#### 8.2.3 捕获诊断消息

为了监听错误消息,需要安装一个 DiagnosticListener。这个监听器在编译器报告警告或

错误消息时会收到一个 Diagnostic 对象。DiagnosticCollector 类实现了这个接口,它将收集所有的诊断信息,使你可以在编译完成之后遍历这些信息。

```
DiagnosticCollector<JavaFileObject> collector = new DiagnosticCollector<>();
compiler.getTask(null, fileManager, collector, null, null, sources).call();
for (Diagnostic<? extends JavaFileObject> d : collector.getDiagnostics())
{
    System.out.println(d);
}
```

Diagnostic 对象包含有关问题位置的信息(包括文件名、行号和列号)以及人类可阅读的描述。 还可以在标准的文件管理器上安装一个 DiagnosticListener 对象,这样就可以捕获到有关 文件缺失的消息:

```
StandardJavaFileManager fileManager
= compiler.getStandardFileManager(diagnostics, null, null);
```

#### 8.2.4 从内存中读取源文件

如果动态地生成了源代码,那么就可以从内存中获取它来进行编译,而无须在磁盘上保存文件。可以使用下面的类来持有代码:

```
public class StringSource extends SimpleJavaFileObject
{
    private String code;
    StringSource(String name, String code)
    {
        super(URI.create("string:///" + name.replace('.','/') + ".java"), Kind.SOURCE);
        this.code = code;
    }
    public CharSequence getCharContent(boolean ignoreEncodingErrors)
    {
        return code;
    }
}

然后,生成类的代码,并提交给编译器一个 StringSource 对象的列表:
List<StringSource> sources = List.of(
        new StringSource(className1, class1CodeString), . . .);
task = compiler.getTask(null, fileManager, diagnostics, null, null, sources);
```

#### 8.2.5 将字节码写出到内存中

如果动态地编译类,那么就无须将类文件写出到硬盘上。可以将它们存储在内存中,并立即加载它们。

```
首先,要有一个类来持有这些字节:

public class ByteArrayClass extends SimpleJavaFileObject
{
    private ByteArrayOutputStream out;
```

```
ByteArrayClass(String name)
     super(URI.create("bytes:///" + name.replace('.','/') + ".class"), Kind.CLASS);
   public byte[] getCode()
      return out.toByteArray();
   public OutputStream openOutputStream() throws IOException
      out = new ByteArrayOutputStream();
      return out;
接下来,需要将文件管理器配置为使用这些类作为输出:
List<ByteArrayClass> classes = new ArrayList<>();
StandardJavaFileManager stdFileManager
   = compiler.getStandardFileManager(null, null, null);
JavaFileManager fileManager
   = new ForwardingJavaFileManager<JavaFileManager>(stdFileManager)
         public JavaFileObject getJavaFileForOutput(Location location,
               String className, Kind kind, FileObject sibling)
               throws IOException
            if (kind == Kind.CLASS)
               ByteArrayClass outfile = new ByteArrayClass(className);
               classes.add(outfile);
               return outfile;
               return super.getJavaFileForOutput(location, className, kind, sibling);
      }:
为了加载这些类、需要使用类加载器(参见第10章):
 public class ByteArrayClassLoader extends ClassLoader
 {
   private Iterable<ByteArrayClass> classes;
   public ByteArrayClassLoader(Iterable<ByteArrayClass> classes)
      this.classes = classes;
    public Class<?> findClass(String name) throws ClassNotFoundException
      for (ByteArrayClass cl : classes)
         if (cl.getName().equals("/" + name.replace('.','/') + ".class"))
```

```
{
           byte[] bytes = cl.getCodeO;
           return defineClass(naine, bytes, 0, bytes.length);
        }
      }
      throw new ClassNotFoundException(name);
   }
}
编译完成后 上面的类加 器调用Class.forName方法
ByteArrayClassLoader loader = new ByteArrayClassLoader(classes);
Class<?> cl = Class.forName(classNamef true, loader);
```

### *8.2.6 <sup>例</sup> 动态Java<sup>代</sup> <sup>成</sup>*

*在 于动态Web JSP技术中 可以在HTML中混杂Java代 例如 <p>The current date and time is <bx%= new java.util.Date() %x/b>.</p>*

*JSP引擎动态地将Java代码编译成Servlet。在 例应 中 我们使 了一个更 单 例 它可以动态 成Swing代 。其基本思想是使 GUI构建器在 体中放 构件 并在 一个外 文件中指定构件 为。 序清单8-4展 了一个 常 单的窗体 实例 序 清单8-5展 了按 动作 代 。 注意 体 构 器 了抽 方法addEventHandlers<sup>o</sup> 我们 代 成器将产 一个实 了 addEventHandlers方法 子 并且对action.properties文 件中 每一行都添加了动作 听器。(我们 下了一个典型 习 即扩展代 成 功 使其支持其他 事件 型。)*

*我们将 个子 于名字为x 包中 因为我们不希望在 序 其他地方 到它。所 成 代 有如下形式*

```
package x;
public class Frame extends SuperclassName
{
   protected void addEventHandlersO
   {
      componentName\.addActionListener(event •>
         {
            code for event handler^
         })
      // repeat for the other event handlers . •.
   }
}
```

*序清单8-3的程序中 buildSource方法构建了 些代 并将它们放到了 StringBuilder-JavaSource <sup>X</sup>寸 中。 对 会传 Java 器。*

*如前一 <sup>所</sup> 我们使 <sup>了</sup>—FonardingJavaFileManager<sup>对</sup> 它会为每一个编译过的类都 构 一个ByteArrayClass对 些对 会捕 x.Franie 时所 成 文件。 方法将每 个文件对象都添加到了一个列 中 然后将其 回 以使我们 后可以定位 些字 。*

*编译完成后 我们使 前一 中描 加 器来加 存储在 个列 中 所有 。然*

#### 后,我们构造并显示应用程序的窗体类。

```
var loader = new ByteArrayClassLoader(classFileObjects);
var frame = (JFrame) loader.loadClass("x.Frame").getConstructor().newInstance();
frame.setVisible(true);
```

当点击按钮时,背景色会按照常规方式进行修改。为了查看这些动作是动态编译的,可以更改 action.properties 文件中一行,例如,修改成下面这样:

yellowButton=panel.setBackground(java.awt.Color.YELLOW); yellowButton.setEnabled(false);

再次运行这个程序,现在,黄色按钮在点击之后就变得禁用了。再看看代码目录,你会 发现 x 包中没有任何源文件和类文件。这个示例向你演示了如何通过内存中的源文件和类文 件来使用动态编译。

#### 程序清单 8-3 compiler/CompilerTest.java

```
1 package compiler;
2
3 import java.awt.*;
4 import java.io.*;
   import java.nio.charset.*;
6 import java.nio.file.*;
7 import java.util.*;
   import java.util.List;
q
   import javax.swing.*:
10
   import javax.tools.*;
11
   import javax.tools.JavaFileObject.*;
12
13
   /**
14
    * @version 1.10 2018-05-01
15
    * @author Cay Horstmann
17
   public class CompilerTest
18
19
      public static void main(final String[] args)
20
            throws IOException, ReflectiveOperationException
21
22
         JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
23
24
         var classFileObjects = new ArrayList<ByteArrayClass>();
25
26
         var diagnostics = new DiagnosticCollector<JavaFileObject>();
27
28
         JavaFileManager fileManager = compiler.getStandardFileManager(diagnostics, null, null);
29
          fileManager = new ForwardingJavaFileManager<JavaFileManager>(fileManager)
38
            {
37
                public JavaFileObject getJavaFileForOutput(Location location.
32
                      String className, Kind kind, FileObject sibling) throws IOException
33
34
                   if (kind == Kind.CLASS)
35
                   {
36
                      var fileObject = new ByteArrayClass(className);
37
                      classFileObjects.add(fileObject);
38
```

```
return fileObject;
39
48
                  else return super.getJavaFileForOutput(location, className, kind, sibling);
41
               }
42
            };
43
45
         String frameClassName = args.length == 0 ? "buttons2.ButtonFrame" : args[0];
45
         //compiler.run(null, null, frameClassName.replace(".", "/") + ".java");
47
48
         StandardJavaFileManager fileManager2 = compiler.getStandardFileManager(null, null);
49
         var sources = new ArrayList<JavaFileObject>();
5A
         for (JavaFileObject o : fileManager2.getJavaFileObjectsFromStrings(
51
               List.of(frameClassName.replace(".", "/") + ".java")))
57
            sources.add(o);
53
54
         JavaFileObject source = buildSource(frameClassName);
         JavaCompiler.CompilationTask task = compiler.getTask(null, fileManager, diagnostics,
56
            null, null, List.of(source));
57
         Boolean result = task.call();
59
69
         for (Diagnostic<? extends JavaFileObject> d : diagnostics.getDiagnostics())
            System.out.println(d.getKind() + ": " + d.getMessage(null));
         fileManager.close();
62
         if (!result)
63
         {
            System.out.println("Compilation failed.");
65
            System.exit(1);
66
         }
67
68
         var loader = new ByteArrayClassLoader(classFileObjects):
69
         var frame = (JFrame) loader.loadClass("x.Frame").getConstructor().newInstance();
70
71
         EventQueue.invokeLater(() ->
72
            {
73
               frame.setDefaultCloseOperation(JFrame.EXIT ON CLOSE);
74
               frame.setTitle("CompilerTest");
75
               frame.setVisible(true);
76
            1):
77
      }
78
79
8A
       * Builds the source for the subclass that implements the addEventHandlers method.
81
82
       * @return a file object containing the source in a string builder
       */
83
      static JavaFileObject buildSource(String superclassName)
84
            throws IOException, ClassNotFoundException
85
RE
         var builder = new StringBuilder();
87
         builder.append("package x;\n\n");
         builder.append("public class Frame extends " + superclassName + " {\n");
89
         builder.append("protected void addEventHandlers() {\n");
98
         var props = new Properties();
91
         props.load(Files.newBufferedReader(
92
93
            Path.of(superclassName.replace(".", "/")).getParent().resolve("action.properties"),
```

```
StandardCharsets.UTF 8));
94
         for (Map.Entry<Object, Object> e : props.entrySet())
95
96
            var beanName = (String) e.getKey();
97
            var eventCode = (String) e.getValue();
98
            builder.append(beanName + ".addActionListener(event -> {\n");
99
            builder.append(eventCode);
100
            builder.append("\n} );\n");
181
102
         builder.append("} }\n");
103
         return new StringSource("x.Frame", builder.toString());
184
105
106 }
```

#### 程序清单 8-4 buttons2/ButtonFrame.java

```
package buttons2;
2 import javax.swing.*;
4 /**
5
    * A frame with a button panel.
    * @version 1.00 2007-11-02
    * @author Cay Horstmann
8
9
   public abstract class ButtonFrame extends JFrame
10 {
      public static final int DEFAULT WIDTH = 300;
11
      public static final int DEFAULT HEIGHT = 200;
12
13
      protected JPanel panel;
14
      protected JButton yellowButton;
15
      protected JButton blueButton;
16
      protected JButton redButton;
17
18
      protected abstract void addEventHandlers();
19
28
      public ButtonFrame()
21
22
23
         setSize(DEFAULT WIDTH, DEFAULT HEIGHT);
24
         panel = new JPanel();
25
         add(panel);
26
27
         yellowButton = new JButton("Yellow");
28
         blueButton = new JButton("Blue");
29
         redButton = new JButton("Red");
30
31
         panel.add(vellowButton);
32
         panel.add(blueButton);
33
         panel.add(redButton);
34
35
         addEventHandlers();
36
37
38
```

#### 366

#### 程序清单 8-5 buttons2/action.properties

- 1 yellowButton=panel.setBackground(java.awt.Color.YELLOW);
- plueButton=panel.setBackground(java.awt.Color.BLUE);

#### API javax.tools.Tool

int run(InputStream in, OutputStream out, OutputStream err, String... arguments)
 用给定的输入、输出、错误流,以及给定的参数来运行该工具。返回值为 0 表示成功,非 0 值表示失败。

#### API javax.tools.JavaCompiler

- StandardJavaFileManager getStandardFileManager(DiagnosticListener<? super JavaFileObject> diagnosticListener, Locale locale, Charset charset)
   获取该编译器的标准文件管理器。如果要使用默认的错误报告机制、locale 和字符集等参数,则可以提供 null。
- JavaCompiler.CompilationTask getTask(Writer out, JavaFileManager fileManager, DiagnosticListener<? super JavaFileObject> diagnosticListener, Iterable<String> options, Iterable<String> classesForAnnotationProcessing, Iterable<? extends JavaFileObject> sourceFiles)

获取编译任务,在被调用时,该任务将编译给定的源文件。参见前一节中有关这部分 内容的详细讨论。

#### API javax.tools.StandardJavaFileManager

- Iterable<? extends JavaFileObject> getJavaFileObjectsFromStrings(Iterable<String> fileNames)
- Iterable<? extends JavaFileObject> getJavaFileObjectsFromPaths(Collection<? extends Path> paths)
- Iterable<? extends JavaFileObject> getJavaFileObjectsFromFiles(Iterable<? extends File> files)

将文件名或文件序列转译成一个 JavaFileObject 实例序列。

#### API javax.tools.JavaCompiler.CompilationTask

Boolean call() 执行编译任务。

#### API javax.tools.DiagnosticCollector<S> 6

- DiagnosticCollector()构造一个空收集器。
- List<Diagnostic<? extends S>> getDiagnostics()
   获取收集到的诊断信息。

#### API javax.tools.Diagnostic<S> 6

- S getSource()
   获取与该诊断信息相关联的源对象。
- Diagnostic.Kind getKind()
   获取该诊断信息的类型,返回值为 ERROR, WARNING, MANDATORY\_WARNING, NOTE 或 OTHER 之一。
- String getMessage(Locale locale)
   获取一条消息,这条消息描述了由该诊断信息所揭示的问题。如果要使用默认的 locale,则传递 null。
- long getLineNumber()
- long getColumnNumber()
   获取由该诊断信息所揭示的问题的位置。

#### API javax.tools.SimpleJavaFileObject

- CharSequence getCharContent(boolean ignoreEncodingErrors)
   对于表示源文件并产生源代码的文件对象,需要覆盖该方法。
- OutputStream openOutputStream()对于表示类文件并产生字节码可写入其中的流的文件对象,需要覆盖该方法。

#### parax.tools.ForwardingJavaFileManager<M extends JavaFileManager>

- protected ForwardingJavaFileManager(M fileManager)
   构造一个 JavaFileManager, 它将所有的调用都代理给指定的文件管理器。
- FileObject getFileForOutput(JavaFileManager.Location location, String className, JavaFileObject.Kind kind, FileObject sibling)
   如果希望替换用于写出类文件的文件对象,则需要拦截该调用。kind 的值是 SOURCE, CLASS, HTML 或 OTHER 之一。

#### 8.3 使用注解

注解是那些插入到源代码中使用其他工具可以对其进行处理的标签。这些工具可以在源码层次上进行操作,或者可以处理编译器在其中放置了注解的类文件。

注解不会改变程序的编译方式。Java 编译器对于包含注解和不包含注解的代码会生成相同的虚拟机指令。

为了能够受益于注解,你需要选择一个处理工具,然后向你的处理工具可以理解的代码中插入注解,之后运用该处理工具处理代码。

注解的使用范围还是很广泛的,并且这种广泛性让人乍一看会觉得有些杂乱无章。下面 是关于注解的一些可能的用法:

- 附属文件的自动生成,例如部署描述符或者 bean 信息类。
- 测试、日志、事务语义等代码的自动生成。

#### *8.3.1<sup>注</sup> <sup>介</sup>*

*我们 先介 基本概念 然后将 些概念 到一个具体 例中 我们将某些方法标注 为AWT构件 事件 听器 然后向你展 一个 够分析注 和 接 听器 注 处 器。 然后 我们对其 法 则 。最后我们以两个注 处 例 束本 。其 中一个可以处 源代码级别 注 另外一个使 了 Apache 字 工 库 可以向注 解过的方法中添加 外 字节码。*

*下 是一个 单注 例*

```
public class MyClass
{
      事
   @Test public void checkRandomlnsertions()
}
```

*注 @Test 于注 checkRandomlnsertions 方法。*

*在Java中 注 是当作修 来使 它 于 注 之前 中 没有分号。(修 饰符就是 如public和static之 关 。)每一个注 名 前 加上了 @ 号 有 点 似于Javadoc 注 。然 Javadoc注 出 在/\*\*...\*/定界符的内 注 是代 一 分。*

*@Test注 并不会做任何事情 它 工具支持才会有 。例如 当测 一个 时 候 JUnit测 工具(可以从http://junit.org处 得)会 所有标 为@Test 方法。另一 个工具可 会删 一个 文件中 所冇测 方法 以便在对 个 测 完毕后 不会将 些 测 方法与 序 在一 。*

*注 可以定义成包含元 形式 例如*

```
@Test(timeout="10090")
```

*些元 可以 取 些注 工具去处 。 有其他形式 元 我们将会在本 后 分 。*

*了方法外 可以注解类、成员以及局 变 些注 可以存在于任何可以放 一 个像pubUc或 static 样 修 地方。另外 正如在8.4 中 到 你 可以注 包、参数变 、 型参数和 型 法。*

*每个注解都必须通过一个注 接口进行定义。 些接口中 方法与注 中 元 对 应。例如 JUnit 注 Test可以 下 个接口 定义*

```
@Target(ElementType.METHOD)
^Retention(RetentionPolicy•RUNTIME)
public ^interface Test
{
   long timeout() default 0L;
     •蠢
}
```

*interface声明创建了一个 正 Java接口。处 注 工具将接收 些实 了 个注*

*接口 对 。 工具可以 timeout方法来 取某个 定Test注 timeout元 。*

*<sup>注</sup> Target和Retention是元注 。它们注 f Test<sup>注</sup> 即将Test<sup>注</sup> <sup>标</sup> 成一个只 到方法上 注 并且当 文件 人到 拟机 时候 它仍可以保 下来。我们将在 8.5.2 些元注 。*

*你 在已 清楚了 序 元数据和注 两个概念。在接下来 小 中 我们将深人到 一个注 处 具体 例中 探 。*

*<sup>注</sup> 对于注 人入 法 可以查 JCommander (http://jconmander.org)和picocli (http://picocli.info)。 些 库将注 于命令 参数 处 。*

#### *8.3.2 例 <sup>注</sup> 事件处 <sup>器</sup>*

*在 户界面编程中 一件更令人 厌 事情就是 事件源上 听器。很多 听器是 下面这种形式*

*myButton.addActionListener(() •> doSomethingd);*

*在本 我们 了一个注 来免 差事。 注 是在 序清单8-8中定义 其使 方式如下*

*@ActionListenerFor(source="myButton") void doSomethingO { . . . }*

*序员不再需要去调用addActionListener 了 是将每个方法 接 一个注 标 。 序清单8-7<sup>展</sup> 了卷I <sup>10</sup>章的ButtonFrame <sup>序</sup> 但是使 <sup>上</sup> <sup>注</sup> 新实 <sup>了</sup> 一 。*

*我们 定义一个注 接口 代 在 序清单8-6中。*

*当然 些注 本 不会做任何事情 它们只是存在于源文件中。 器将它们 于 文件中 并且 拟机会将它们 入。我们 在 是一个分析注 以及安 为 听器 机制。 也是 ActionListenerlnstaUer的职责所在。ButtonFrame构 器将 下 方法*

*ActionListenerlnstaUer.processAnnotations(this);*

*态 processAnnotations方法可以枚举出某个对 接收到 所有方法。对于每一个方法 它先 取ActionListenerFor注 对 然后再对它 处 <sup>o</sup>*

```
Class<?> cl = obj.getClassO;
for (Method m : cl.getDeclaredMethods())
{
   ActionListenerFor a = m.getAnnotation(ActionListenerFor.class); 
   if (a != null)...
}
```

*这里 我们使 了定义在 AnnotatedElement 接 口中 getAnnotation 方法。Method .Constructor、 Field、Class和Package 些 实 了 个接口。*

*源成员域 名字是存储在注 对 中 。我们可以 source方法对它 检 然后査找匹配的成员域。*

String fieldName = a.source();
Field f = cl.getDeclaredField(fieldName);

这表明我们的注解有一个限制条件,即源元素必须是一个成员域的名字,而不能是局部变量。 代码的剩余部分相当具有技术性。对于每一个被注解的方法,我们构造了一个实现了 ActionListener 接口的代理对象,其 actionPerformed 方法将调用这个被注解过的方法。(关于代理的更多信息见卷 I 第 6 章。)细节并不重要,关键要知道注解的功能是通过 processAnnotations 方法建立起来的。

图 8-1 展示了在本例中注解是如何被处理的。

在这个示例中,注解是在运行时进行处理的。另外也可以在源码级别上对它们进行处理,这样,源代码生成器将产生用于添加监听器的代码。注解也可以在字节码级别上进行处理,字节码编辑器可以将对 addActionListener 的调用注入框体构造器中。听起来似乎很复杂,不过可以利用一些类库相对直截了当地实现这项任务。

对于用户界面程序员来说,我们这个示例并不能看作是一个严格意义上的工具。因为,用于添加监听器的实用方法对于程序员来说和添加一条注解一样方便。(实际上, java.beans. EventHandler 类试图实现的就是这样。通过在这个类中提供一个可以添加事件处理器的方法,而不只是构建它,就可以很容易地对它进行改进。)

![](_page_163_Figure_7.jpeg)

图 8-1 在运行时处理注解

不过,这个示例展示了对一个程序进行注解以及对这些注解进行分析的机制。既然你已经领会了这个具体示例,那么,现在可能已经为后续小节详述注解语法做好了更充分的准备(这也是我们所希望的)。

#### 程序清单 8-6 runtimeAnnotations/ActionListenerInstaller.java

- package runtimeAnnotations;
- 3 import java.awt.event.\*;
- 4 import java.lang.reflect.\*;

5

```
6 /**
    * @version 1.00 2004-08-17
    * @author Cay Horstmann
9
   public class ActionListenerInstaller
10
11
12
       * Processes all ActionListenerFor annotations in the given object.
13
       * @param obj an object whose methods may have ActionListenerFor annotations
14
15
      public static void processAnnotations(Object obj)
16
17
         try
18
         {
19
             Class<?> cl = obj.getClass();
             for (Method m : cl.getDeclaredMethods())
21
22
                ActionListenerFor a = m.getAnnotation(ActionListenerFor.class);
23
                if (a != null)
25
                   Field f = cl.getDeclaredField(a.source());
26
                   f.setAccessible(true):
27
                   addListener(f.get(obj), obj, m);
28
29
38
31
          catch (ReflectiveOperationException e)
32
33
             e.printStackTrace();
34
35
       }
36
37
       /**
38
        * Adds an action listener that calls a given method.
39
        * @param source the event source to which an action listener is added
48
        * @param param the implicit parameter of the method that the listener calls
41
        * @param m the method that the listener calls
42
        */
43
       public static void addListener(Object source, final Object param, final Method m)
44
             throws ReflectiveOperationException
45
46
          var handler = new InvocationHandler()
47
48
             {
                public Object invoke(Object proxy, Method mm, Object[] args) throws Throwable
40
58
                   return m.invoke(param);
51
52
             };
53
54
          Object listener = Proxy.newProxyInstance(null,
55
             new Class[] { java.awt.event.ActionListener.class }, handler);
56
          Method adder = source.getClass().getMethod("addActionListener", ActionListener.class);
57
          adder.invoke(source, listener);
58
59
60 }
```

#### 程序清单 8-7 buttons3/ButtonFrame.java

```
package buttons3;
2
3 import java.awt.*;
4 import javax.swing.*;
5 import runtimeAnnotations.*;
7
   * A frame with a button panel.
   * @version 1.00 2004-08-17
   * @author Cay Horstmann
11
   public class ButtonFrame extends JFrame
12
13
      private static final int DEFAULT WIDTH = 300;
14
      private static final int DEFAULT_HEIGHT = 200;
15
16
      private JPanel panel;
17
      private JButton yellowButton;
18
19
      private JButton blueButton;
      private JButton redButton;
20
21
      public ButtonFrame()
23
24
         setSize(DEFAULT_WIDTH, DEFAULT_HEIGHT);
25
         panel = new JPanel();
26
         add(panel);
27
28
         yellowButton = new JButton("Yellow");
29
30
         blueButton = new JButton("Blue");
         redButton = new JButton("Red");
31
32
         panel.add(yellowButton);
33
         panel.add(blueButton);
34
         panel.add(redButton);
35
         ActionListenerInstaller.processAnnotations(this);
37
38
39
      @ActionListenerFor(source = "yellowButton")
48
41
      public void yellowBackground()
42
         panel.setBackground(Color.YELLOW);
43
44
45
      @ActionListenerFor(source = "blueButton")
46
47
      public void blueBackground()
      {
48
          panel.setBackground(Color.BLUE);
49
50
51
52
      @ActionListenerFor(source = "redButton")
```

```
public void redBackground()

{
    panel.setBackground(Color.RED);
}
```

#### 程序清单 8-8 runtimeAnnotations/ActionListenerFor.java

```
package runtimeAnnotations;
\nimport java.lang.annotation.*;

/**
    * @version 1.00 2004-08-17
    * @author Cay Horstmann
    */
    @Target(ElementType.METHOD)
    @Retention(RetentionPolicy.RUNTIME)
public @interface ActionListenerFor
{
    String source();
}
```

#### API java.lang.reflect.AnnotatedElement 5.0

- boolean isAnnotationPresent(Class<? extends Annotation> annotationType)
   如果该项具有给定类型的注解,则返回 true。
- <T extends Annotation> T getAnnotation(Class<T> annotationType)
   获得给定类型的注解,如果该项不具有这样的注解,则返回 null。
- <T extends Annotation> T[] getAnnotationsByType(Class<T> annotationType) 8
   获得某个可重复注解类型的所有注解(查阅 8.5.2 节),或者返回长度为 0 的数组。
- Annotation[] getAnnotations()
   获得作用于该项的所有注解,包括继承而来的注解。如果没有出现任何注解,那么将返回一个长度为0的数组。
- Annotation[] getDeclaredAnnotations()
   获得为该项声明的所有注解,不包含继承而来的注解。如果没有出现任何注解,那么 将返回一个长度为 0 的数组。

#### 8.4 注解语法

本节将介绍你必须了解的注解语法。

#### 8.4.1 注解接口

注解是由注解接口来定义的:

```
modifiers @interface AnnotationName
{
    elementDeclaration1
    elementDeclaration2
}
每个元素声明都具有下面这种形式:
type elementName();

或者

type elementName() default value;
例如,下面这个注解具有两个元素: assignedTo 和 severity。
public @interface BugReport
{
    String assignedTo() default "[none]";
    int severity();
}
```

所有的注解接口都隐式地扩展自 java.lang.annotation.Annotation 接口。这个接口是一个常规接口,不是一个注解接口。请查看本节最后为该接口提供的一些方法所做的 API 注释。

你无法扩展注解接口。换句话说,所有的注解接口都直接扩展自 java.lang.annotation. Annotation。你也从来不用为注解接口提供实现类。

注解接口的方法没有参数也没有 throws 子句,它们不能是 default 或 static 方法,也不能有类型参数。

注解元素的类型为下列之一:

- 基本类型 (int、short、long、byte、char、double、float 或者 boolean)。
- String。
- Class (具有一个可选的类型参数,例如 Class<? extends MyClass)。
- enum 类型。
- 注解类型。
- 由前面所述类型组成的数组(由数组组成的数组不是合法的元素类型)。

下面是一些合法的元素声明的例子:

```
public @interface BugReport
{
   enum Status { UNCONFIRMED, CONFIRMED, FIXED, NOTABUG };
   boolean showStopper() default false;
   String assignedTo() default "[none]";
   Class<?> testCase() default Void.class;
   Status status() default Status.UNCONFIRMED;
   Reference ref() default @Reference(); // an annotation type
   String[] reportedBy();
}
```

#### API java.lang.annotation.Annotation 5.0

- Class<? extends Annotation> annotationType() 返回 Class 对象,它用于描述该注解对象的注解接口。注意:调用注解对象上的 getClass 方法返回的是真正的类,而不是接口。
- boolean equals(Object other)
   如果 other 是一个实现了与该注解对象相同的注解接口的对象,并且如果该对象和 other 的所有元素彼此相等。那么返回 True。
- int hashCode() 返回一个与 equals 方法兼容、由注解接口名以及元素值衍生而来的散列码。
- String toString()
   返回一个包含注解接口名以及元素值的字符串表示,例如,@BugReport (assignedTo= [none], severity=θ)。

#### 8.4.2 注解

每个注解都具有下面这种格式:

@AnnotationName(elementName1=value1, elementName2=value2, . . .)

例如,

@BugReport(assignedTo="Harry", severity=10)

元素的顺序无关紧要。下面这个注解和前面那个一样。

@BugReport(severity=10, assignedTo="Harry")

如果某个元素的值并未指定,那么就使用声明的默认值。例如,考虑一下下面这个注解: @BugReport(severity=10)

元素 assignedTo 的值是字符串 "[none]"。

● 警告: 默认值并不是和注解存储在一起的;相反地,它们是动态计算而来的。例如,如果你将元素 assignedTo 的默认值更改为 "[]",然后重新编译 BugReport 接口,那么注解 @BugReport(severity=10) 将使用这个新的默认值,甚至在那些在默认值修改之前就已经编译过的类文件中也是如此。

有两个特殊的快捷方式可以用来简化注解。

如果没有指定元素,要么是因为注解中没有任何元素,要么是因为所有元素都使用默认 值,那么你就不需要使用圆括号了。例如,

@BugReport

和下面这个注解是一样的

@BugReport(assignedTo="[none]", severity=θ)

这样的注解又称为标记注解。

另外一种快捷方式是单值注解。如果一个元素具有特殊的名字 value,并且在注解中没有指定其他元素,那么你就可以忽略掉这个元素名以及等号。例如,既然我们已经在前面将 Action ListenerFor 注解接口定义为如下形式:

```
public @interface ActionListenerFor
{
    String value();
}
```

那么,我们可以将这个注解书写成如下形式:

@ActionListenerFor("vellowButton")

#### 而不是

@ActionListenerFor(value="yellowButton")

一个项可以有多个注解:

@Test

@BugReport(showStopper=true, reportedBy="Joe")
public void checkRandomInsertions()

如果注解的作者将其声明为可重复的,那么你就可以多次重复使用同一个注解:

```
@BugReport(showStopper=true, reportedBy="Joe")
@BugReport(reportedBy={"Harry", "Carl"})
public void checkRandomInsertions()
```

- 直 注释: 因为注解是由编译器计算而来的,因此,所有元素值必须是编译期常量。例如,
  @BugReport(showStopper=true, assignedTo="Harry", testCase=MyTestCase.class,
  status=BugReport.Status.CONFIRMED, . . .)
- 警告: 一个注解元素永远不能设置为 null, 甚至不允许其默认值为 null。这样在实际应用中会相当不方便。你必须使用其他的默认值,例如 ""或者 Void.class。

如果元素值是一个数组,那么要将它的值用括号括起来,像下面这样:

@BugReport(. . ., reportedBy={"Harry", "Carl"})

如果该元素具有单值,那么可以忽略这些括号:

@BugReport(. . ., reportedBy="Joe") // OK, same as {"Joe"}

既然一个注解元素可以是另一个注解,那么就可以创建出任意复杂的注解。例如,

@BugReport(ref=@Reference(id="3352627"), . . .)

直 注释: 在注解中引入循环依赖是一种错误。例如,因为 BugReport 具有一个注解类型为 Reference 的元素,所以 Reference 就不能再拥有一个类型为 BugReport 的元素。

#### 8.4.3 注解各类声明

注解可以出现在许多地方,这些地方可以分为两类:声明和类型用法。声明注解可以出

#### 现在下列声明处:

- · 句
- · 类 (包括 enum)
- 接口(包括注解接口)
- 方法
- 构造器
- 实例域 (包含 enum 常量)
- 局部变量
- 参数变量
- 类型参数

对于类和接口,需要将注解放置在 class 和 interface 关键词的前面:

```
@Entity public class User { . . . }
```

对于变量,需要将它们放置在类型的前面:

```
@SuppressWarnings("unchecked") List<User> users = . . .;
public User getUser(@Param("id") String userId)
```

泛化类或方法中的类型参数可以像下面这样被注解:

```
public class Cache<@Immutable V> { . . . }
```

包是在文件 package-info. java 中注解的,该文件只包含以注解先导的包语句。

```
/**
    Package-level Javadoc
*/
@GPL(version="3")
package com.horstmann.corejava;\nimport org.gnu.GPL;
```

直 注释:对局部变量的注解只能在源码级别上进行处理。类文件并不描述局部变量。因此,所有的局部变量注解在编译完一个类的时候就会被遗弃掉。同样地,对包的注解不会在源码级别之外存在。

#### 8.4.4 注解类型用法

声明注解提供了正在被声明的项的相关信息。例如,在下面的声明中 public User getUser(@NonNull String userId)

就断言 userId 参数不为空。

i 注释: @NonNull 注解是 Checker Framework 的一部分 (https://checkerframework.org)。通过使用这个框架,可以在程序中包含断言,例如某个参数不为空,或者某个 String 包含一个正则表达式。然后,静态分析工具将检查在给定的源代码段中这些断言是否有效。

现在, 假设我们有一个类型为 List<String> 的参数, 并且想要表示其中所有的字符串都

不为 null。这就是类型用法注解大显身手之处,可以将该注解放置到类型参数之前: List ← NonNull String>。

类型用法注解可以出现在下面的位置:

- 与泛化类型参数一起使用: List<@NonNull String>, Comparator.<@NonNull String> reverseOrder()。
- 数组中的任何位置: @NonNull String[][] words (words[i][j] 不为 null), String @NonNull [][]
   words (words 不为 null), String[] @NonNull [] words (words[i] 不为 null)。
- 与超类和实现接口一起使用: class Warning extends @Localized Message。
- 与构造器调用一起使用: new @Localized String(...)。
- 与强制转型和 instanceof 检查一起使用: (@Localized String) text, if (text instanceof @Localized String)。(这些注解只供外部工具使用,它们对强制转型和 instanceof 检查不会产生任何影响。)
- 与异常规约一起使用: public String read() throws @Localized IOException。
- 与通配符和类型边界一起使用: List<@Localized ? extends Message>, List<? extends @Localized Message>。
- 与方法和构造器引用一起使用: @Localized Message::getText。

有多种类型位置是不能被注解的:

@NonNull String.class // ERROR: Cannot annotate class literal import java.lang.@NonNull String; // ERROR: Cannot annotate import

可以将注解放置到诸如 private 和 static 这样的其他修饰符的前面或后面。习惯(但不是必需)的做法,是将类型用法注解放置到其他修饰符的后面和将声明注解放置到其他修饰符的前面。例如,

private @NonNull String text; // Annotates the type use
@Id private String userId; // Annotates the variable

在注解一个记录构件时,可以将注解应用于生成的域、getter方法或构造器参数上。

直 注释: 注解的作者需要指定特定的注解可以出现在哪里。如果一个注解可以同时应用于变量和类型用法,并且它确实被应用到了某个变量声明上,那么该变量和类型用法就都被注解了。例如,请考虑

public User getUser(@NonNull String userId)

如果@NonNull 可以同时应用于参数和类型用法,那么 userId 参数就被注解了,而其参数类型是 @NonNull String。

#### 8.4.5 注解 this

```
假设想要将参数注解为在方法中不会被修改。

public class Point {
    public boolean equals(@ReadOnly Object other) { . . . }
}
```

*么 处 个注 工具在 到下 时 p.equals(q)*

*就会推 出q没有 修改 。*

*但是P呢*

*当 方法 时 this变 是 定到p 。但是this从来 没有 声明 因此你无 法注 它。*

*实 上 你可以 一 很少使 法变体来声明它 样你就可以添加注 了*

```
public class Point
{
   public boolean equals(^Readonly Point this, ^Readonly Object other) { . . . }
}
```

*一个参数 为接收器参数 它必 命名为this, <sup>它</sup> 型就是 构建 。*

*0 <sup>注</sup> 你只 为方法 <sup>不</sup> 为构 器提供接收器参数。从概念上 <sup>构</sup> 器中 this 引 在构 器没有执 完之前 不是 定 型 对 。所以 放 在构 器上 注 描 是 构建 对 属性。*

*传 内 构 器 是另一个不同 参数 即对其外围 对 引 。你也可以 个参数显式化*

```
public class Sequence
{
   private int frora;
   private int to;
   class Iterator implements java.util.Iterator<Integer>
   {
      private int current;
      public Iterator(@ReadOnly Sequence Sequence.this)
      {
         this.current = Sequence.this.from;
}
```

*个参数 名字必 像引 它时 样 叫作EnclosingClass.this,其 型为外围 。*

## *8.5标准注*

*java.lang java.lang.annotation 和 javax.annotation 包中定义了大 注 接口。其中四个 是元注 于描 注 接口 为属性 其他 是 则接口 可以 它们来注 你 源代 中的项。 8-2列出了 些注 。我们将会在 后 两个小 中 予 介 。*

| 注<br>接口             | 应<br>场合            | 目的                                                   |  |
|---------------------|--------------------|------------------------------------------------------|--|
| Deprecated          | 全                  | 将<br>标<br>为<br>时                                     |  |
| SuppressWamings     | 了包和注<br>之外<br>所有情况 | 止某个<br>定<br>型<br>告信息                                 |  |
| SafeVarargs         | 方法和构<br>器          | 断<br>varargs参数可安全使                                   |  |
| Override            | 方法                 | 检査<br>方法是否<br>了某一个<br>方法                             |  |
| serial              | 方法                 | 检査<br>方法是不是正<br>序列化<br>方法                            |  |
| Functionallnterface | 接口                 | 将接口标<br>为只有一个抽<br>方法<br>函数式接                         |  |
| Generated           | 全                  | 将<br>标<br>为<br>某个工具<br>成<br>源代                       |  |
| Target              | 注                  | 指明<br>个注<br>可以应<br>到哪些<br>上                          |  |
| Retention           | 注                  | 指明<br>个注<br>可以保<br>多久                                |  |
| Documented          | 注                  | 指明<br>个注<br>应<br>包含在<br>注解项的文档中                      |  |
| Inherited           | 注                  | 指明当<br>个注<br>应<br>于一个<br>时候<br>够<br>动<br>它<br>子<br>承 |  |
| Repeatable          | 注                  | 指明<br>个注<br>可以在同一个<br>上应<br>多次                       |  |

*8-2标准注*

#### *8.5.1 于编译的注*

*deprecated注 可以 添加到任何不再 励使 上。所以 当你使 一个已 时 时 器将会发出 告。 个注 与Javadoc标 ©deprecated具有同 功效。但是 注 会一 持久化到运行时。*

*H <sup>注</sup> jdeprscan工具可以扫描JAR文件 <sup>中</sup> 时元 它是JDK的组成 <sup>分</sup>。*

*@SuppressWarnings注 会告 器 止 定 型 告信息 例如*

*@SuppressWarnings(\*unchecked )*

*©Override这种注 只 应 到方法上。 器会检査具有 注 方法是否 正 了一个来自超类的方法。例如 如果你声明*

```
public MyClass
{
   ^Override public boolean equals(MyClass other);
   • • •
}
```

*么 器会报告一个 。毕 个equals方法没有 Object equals方法。 因为 个方法有一个 型为Object 不是MyClass 参数。*

*generated注 是供代 成工具来使 。任何 成 源代 可以 注 从 与 序员提供 代 区分开。例如 代 器可以 成 代 或 代 成器可以 移除生成代码的旧 本。每个注 必 包含一个 代 成器 唯一标 日期字 串(ISO8601格式)和注 字 串是可选的。例如*

*@Generated("com.horstmann.beanproperty", M2008-01-04T12:08:56.235-0790");*

#### *8.5.2元注*

*Target元注 可以应 于一个注 以 制 注 可以应 到哪些 上。例如*

*^Target ElementType•TYPE, ElementType.METHOD public ^interface BugReport*

*8-3显 了所有可能的取值情况 它们属于枚举 型ElementType 可以指定任意数 元素类型 括号括 来。*

| 元素类型            | 注<br>场台              | 元素类型          | 注<br>场合        |
|-----------------|----------------------|---------------|----------------|
| ANNOTATION TYPE | 注<br>型声明             | FIELD         | 成员域<br>包括enum常 |
| PACKAGE         | 包                    | PARAMETER     | 方法或构<br>器参数    |
| TYPE            | 包括enum<br>及接口<br>包括注 | LOCALVARIABLE | 局<br>变最        |
| METHOD          | 方法                   | TYPEPARAMETER | 型参数            |
| CONSTRUCTOR     | 构<br>器               | TYPE USE      | 型<br>法         |

*8-3 @Target<sup>注</sup> <sup>元</sup> <sup>型</sup>*

*一条没有@Target 制 注 可以应 于任何 上。 器将检査你是否将一条注 只 应 到了某个允 上。例如 如果将BugReport应 于一个成员域上 则会导 时*

*Retention元注 于指定一条注 应 保 多 时 。只 将其指定为 8-4中 任 意值 其默认值是 RetentionPolicy.CLASS*

| 保<br>则  | 描                                               |
|---------|-------------------------------------------------|
| SOURCE  | 不包括在<br>文件中<br>注                                |
| CLASS   | 包括在<br>文件中<br>注<br>但是<br>拟机不<br>将它们<br>人        |
| RUNTIME | 包括在<br>文件中<br>注<br>并<br>拟机<br>入。通过反射API可<br>得它们 |

*8-4 <sup>于</sup>©Retention<sup>注</sup> <sup>保</sup>*

*<sup>在</sup> 序清单8-8<sup>巾</sup> ©ActionListenerFor<sup>注</sup> 声明为具有RetentionPolicy.RUNTIME,因为我们 是使 反射机制 注 处 。在 后 两个小 你将会 到一些在源码级别和 文 件 别上怎样对注 处 例。*

*@Documented元注 为像Javadoc 样 归档工具提供了一些提 。应 像处 其他修 例如protected和static —样来处 归档注 以实 其归档 。其他注 <sup>使</sup> 并不会 人归档的范畴。例如 假定我们将©ActionListenerFor作为一个归档注 来声明*

*documented*

*^Target ElementType.METHOD* 

*^Retention RetentionPolicy.RUNTIME* 

*public ^interface ActionListenerFor*

现在每一个被该注解标注过的方法的归档就会含有这条注解,如图 8-2 所示。

![](_page_175_Picture_3.jpeg)

图 8-2 归档注解

如果某个注解是暂时性的(例如@BugReport),那么就不应该对它们的用法进行归档。

直注释:将一个注解应用到它自身上是合法的。例如,@Documented 注解被它自身注解为 @Documented。因此,针对注解的 Javadoc 文档可以表明它们是否可被归档。

@Inherited 元注解只能应用于对类的注解。如果一个类具有继承注解,那么它的所有子类都自动具有同样的注解。这使得创建一个与 Serializable 这样的标记接口具有相同运行方式的注解变得很容易。

实际上, @Serializable 注解应该比没有任何方法的 Serializable 标记接口更适用。一个类之所以可以被序列化,是因为存在着对它的成员域进行读写的运行期支持,而不是因为任何面向对象的设计原则。注解比接口继承更擅长描述这一事实。当然,可序列化接口是在JDK1.1 中产生的,远比注解出现得早。

假设定义了一个继承注解@Persistent来指明一个类的对象可以存储到数据库中,那么该持久类的子类就会自动被注解为是持久性的。

```
@Inherited @interface Persistent { }
@Persistent class Employee { . . . }
class Manager extends Employee { . . . } // also @Persistent
```

在持久化机制去查找存储在数据库中的对象时,它就会同时探测到 Employee 对象以及 Manager 对象。

对于 Java 8 来说,将同种类型的注解多次应用于某一项是合法的。为了向后兼容,可重

*复注 实 提供一个容器注 它可以将 些 复注 存储到一个数 中。*

*下 是如何定义@TestCase注 以及它 容器 代*

```
Repeatable (Testcases • class)
^interface Testcase
{
   String paramsO; 
   String expected();
}
^interface TestCases
{
   TestCase[] valued;
}
```

*无 何时 只 户提供了两个或更多个@TestCase注 么它们就会 动地 包 到 一个@TestCases注 中。*

*0 <sup>告</sup> 在处 <sup>可</sup> 复注 时必 常仔 。如果 getAnnotation来查找某个可 复注 注 又 实 复了 么就会得到nuU 是因为 复注 包 到了容器注 中。 在 情况下 应 getAnnotationsByType。 个调用会" 历"容器 并 出一个 复注 数 。如果只有一条注 么 数 度就为1。通过使用这个方法 你就不 操心如何处 容器注 了。*

## *8.6<sup>源</sup> <sup>注</sup> <sup>处</sup>*

*在上一 中 你 到了如何分析正在 序中 注 。注 另一 法是 动处 源代 以产 更多 源代 、 文件、 本或其他任何我们想 成 东 。*

#### *8.6.1<sup>注</sup> <sup>处</sup> <sup>器</sup>*

*注 处 已 成到了 Java 器中。在 中 你可以 下 命令来 注 处 器。*

*javac -processor ProcessorClassName^ <sup>l</sup>ProcessorClassName2l. . . sourceFiles*

*器会定位源文件中 注 。每个注 处 器会依次执 并得到它 感兴 注 。如果某个注 处 器创建了一个新 源文件 么上 将 复执 。如果某次处 循 没有再产 任何新 源文件 么就 所有 源文件。*

*EI<sup>注</sup> <sup>注</sup> <sup>处</sup> 器只 <sup>产</sup> <sup>新</sup> 源文件 它无法修改已有 源文件。*

*注 处 器 常 扩展Abstractprocessor 实 Processor接口。你 指定你 处 器支持 注 我们 案例如下*

*@Suppo rtedAnnotationTypes(<sup>H</sup> cos.ho rstnann.annotations.ToSt ringa) @SupportedSourceVersion(SourceVersion.RELEASE 8)*

```
public class ToStringAnnotationProcessor extends AbstractProcessor
{
   public boolean process(Set<? extends TypeElement> annotations,
```

处理器可以声明具体的注解类型或诸如 "com.horstmann.\*" 这样的通配符(com.horstmann包及其所有子包中的注解), 甚至是 "\*"(所有注解)。

在每一轮中,process 方法都会被调用一次,调用时会传递给由这一轮在所有文件中发现的所有注解构成的集,以及包含了有关当前处理轮次的信息的 RoundEnvironment 引用。

#### 8.6.2 语言模型 API

应该使用语言模型 API 来分析源码级的注解。与用来呈现类和方法的虚拟机表示形式的 反射 API 不同,语言模型 API 让我们可以根据 Java 语言的规则去分析 Java 程序。

编译器会产生一棵树,其节点是实现了 javax.lang.model.element.Element 接口及其 TypeElement、VariableElement、ExecutableElement 等子接口的类的实例。这些节点可以类比于编译时的 Class、Field/Parament 和 Method/Constructor 反射类。

本书并不会详细讨论该 API, 但我们要强调的是, 你需要知道它是如何处理注解的。

RoundEnvironment 通过调用下面的方法交给你一个由特定注解标注过的所有元素构成的集。

Set<? extends Element> getElementsAnnotatedWith(Class<? extends Annotation> a)

在源码级别上等价于 AnnotatedElement 接口的是 AnnotatedConstruct。使用下面的方法就可以获得属于给定注解类的单条注解或重复的注解。

A getAnnotation(Class<A> annotationType)
A[] getAnnotationSByType(Class<A> annotationType)

- TypeElement表示一个类或接口,而 getEnclosedElements方法会产生一个由它的域和方法构成的列表。
- 在 Element 上调用 getSimpleName 或在 TypeElement 上调用 getQualifiedName 会产生一个 Name 对象,它可以用 toString 方法转换为一个字符串。

#### 8.6.3 使用注解来生成源码

作为示例,我们将使用注解来减少实现 toString 方法时枯燥的编程工作量。我们不能将 这些方法放到原来的类中,因为注解处理器只能产生新的类,而不能修改已有的类。

因此,我们将所有方法添加到工具类 ToStrings 中:

```
public class ToStrings
{
   public static String toString(Point obj)
```

```
Generated code
       public static String toString(Rectangle obj)
         Generated code
       public static String toString(Object obj)
         return Objects.toString(obj);
    }
    我们不想使用反射,因此对访问器方法而不是域进行注解:
    @ToString
    public class Rectangle
       @ToString(includeName=false) public Point getTopLeft() { return topLeft; }
       @ToString public int getWidth() { return width; }
       @ToString public int getHeight() { return height; }
    然后, 注解处理器应该生成下面的源码:
    public static String toString(Rectangle obj)
       result, append ("Rectangle");
       result.append(toString(obj.getTopLeft()));
       result.append("width=");
       result.append(toString(obj.getWidth()));
       result append ("height=");
       result.append(toString(ob).getHeight()));
       return result.toString();
    其中,灰色的是"模板"代码。下面的框架所描述的方法可以为具有给定的 TypeElement
的类产生 toString 方法:
     private void writeToStringMethod(PrintWriter out, TypeElement te)
       String className = te.getQualifiedName().toString();
       Print method header and declaration of string builder
       ToString ann = te.getAnnotation(ToString.class);
       if (ann.includeName())
          Print code to add class name
       for (Element c : te.getEnclosedElements())
```

```
ann = c.getAnnotation(ToString.class);\nif (ann != null)
{
    if (ann.includeName()) Print code to add field name
        Print code to append toString(obj.methodName())
    }
}
Print code to return string
}
```

而下面给出的是注解处理器的 process 方法的框架。它会创建助手类的源文件,并为每个被注解标注的类编写类头和一个 toString 方法。

```
public boolean process(Set<? extends TypeElement> annotations,
     RoundEnvironment currentRound)
  if (annotations.size() == 0) return true;
  try
  {
     JavaFileObject sourceFile = processingEnv.getFiler().createSourceFile(
            "com.horstmann.annotations.ToStrings");
     try (var out = new PrintWriter(sourceFile.openWriter()))
         Print code for package and class
         for (Element e : currentRound.getElementsAnnotatedWith(ToString.class))
            if (e instanceof TypeElement te)
               writeToStringMethod(out, te);
         Print code for toString(Object)
     }
     catch (IOException e)
         processingEnv.getMessager().printMessage(
               Kind.ERROR, ex.getMessage());
     }
  return true;
}
```

对于具体的那些显得有些冗长的代码,可以去查看本书附带的代码。

注意, process 方法在后续轮次中是用空的注解列表调用的, 然后, 它会立即返回, 因此它并不会多次创建源文件。

首先,编译注解处理器,然后编译并运行测试程序,就像下面这样:

```
javac sourceAnnotations/ToStringAnnotationProcessor.java
javac -processor sourceAnnotations.ToStringAnnotationProcessor rect/*.java
java rect.SourceLevelAnnotationDemo
```

#### ☑ 提示: 要想查看轮次, 可以用 -XprintRounds 标记来运行 javac 命令:

```
Round 1:
   input files: {rect.Point, rect.Rectangle,
     rect.SourceLevelAnnotationDemo}
   annotations: [sourceAnnotations.ToString]
```

last round: false

Round 2:

input files: {sourceAnnotations.ToStrings}

annotations: [] last round: false

Round 3:

input files: {}
annotations: []
last round: true

这个示例演示了工具可以如何获取源文件注解以产生其他文件。生成的文件并非一定要是源文件。注解处理器可以选择生成 XML 描述符、属性文件、Shell 脚本、HTML 文档等。

直 注释:有些人建议使用注解来完成一项更繁重的体力活。如果琐碎的获取器和设置器可以自动生成,那岂不是很好?例如,用下面的注解:

@Property private String title;

来产生下面的方法:

```
public String getTitle() { return title; }
public void setTitle(String title) { this = title; }
```

但是,这些方法需要被添加到同一个类中。这需要编辑源文件而不是产生另一个文件,而 这超出了注解处理器的能力范围。我们可以为实现此目的而构建另一个工具,但是这种工 具超出了注解的职责范围。注解被设计为对代码项的描述,而不是添加或修改代码的指令。

#### 8.7 字节码工程

你已经看到了我们是怎样在运行期或者在源码级别上对注解进行处理的。还有第3种可能:在字节码级别上进行处理。除非将注解在源码级别上删除,否则它们会一直存在于类文件中。类文件格式是归过档的(参阅 http://docs.oracle.com/javase/specs/jvms/sel0/html),这种格式相当复杂,并且在没有特殊类库支持的情况下,处理类文件具有很大的挑战性。ASM 库就是这样的特殊类库之一,可以从网站 http://asm.ow2.org 上获得。你可以下载 asm-9.2.jar 和 asm-commons-9.2.jar,将它们放到你选择的目录中,在下面的指令中,我们称该目录为 asm。

#### 8.7.1 修改类文件

在本小节,我们使用 ASM 向已注解方法中添加日志信息。如果一个方法被这样注解过:@LogEntry(logger=loggerName)

那么,在方法的开头部分,我们将添加下面这条语句的字节码:

 ${\tt Logger.getLogger}(loggerName). {\tt entering}(className,\ methodName);$ 

例如,如果对 Item 类的 hashCode 方法做了如下注解:

@LogEntry(logger="global") public int hashCode()

那么,在任何时候调用该方法,都会报告一条与下面打印出来的消息相似的消息:

May 17, 2016 10:57:59 AM Item hashCode

FINER: ENTRY

为了实现这项任务, 我们需要遵循下面几点:

- 1. 加载类文件中的字节码。
- 2. 定位所有的方法。
- 3. 对于每个方法,检查它是不是有一个 LogEntry 注解。
- 4. 如果有,在方法开头部分添加下面所列指令的字节码:

ldc loggerName

invokestatic

java/util/logging/Logger.getLogger:(Ljava/lang/String;)Ljava/util/logging/Logger;

ldc className

ldc methodName

invokevirtual

java/util/logging/Logger.entering:(Ljava/lang/String;Ljava/lang/String;)V

插入这些字节码看起来相当棘手,不过 ASM 却使它变得相当简单。我们不会详细描述和分析插入字节码的过程。关键之处是程序清单 8-9 中的程序可以编辑一个类文件,并且在已经用 LogEntry 注解标注过的方法的开头部分插入日志调用。

例如,下面展示了应该怎样向程序清单 8-10 中的 Item. java 文件添加记录日志指令,其中 asm 是安装 ASM 库的目录。

javac set/Item.java
javac -classpath .:asm/\\* bytecodeAnnotations/EntryLogger.java
java -classpath .:asm/\\* bytecodeAnnotations.EntryLogger set.Item

在对 Item 类文件进行修改之前和之后分别试运行一下:

iavap -c set.Item

就可以看到在 hashCode、equals 以及 compareTo 方法的开头部分插入的那些指令。

public int hashCode();

Code:

- 0: ldc #85; // String global
- 2: invokestatic #80;

// Method

// java/util/logging/Logger.getLogger:(Ljava/lang/String;)Ljava/util/logging/Logger;

- 5: ldc #86; //String Item
- 7: ldc #88: //String hashCode
- 9: invokevirtual #84;

// Method java/util/logging/Logger.entering:(Ljava/lang/String;Ljava/lang/String;)V

- 12: bipush 13
- 14: aload 0
- 15: getfield #2; // Field description:Ljava/lang/String;
- 18: invokevirtual #15; // Method java/lang/String.hashCode:()I
- 21: imul
- 22: bipush 17
- 24: aload 0
- 25: getfield #3; // Field partNumber:I
- 28: imul
- 29: iadd
- 30: ireturn

程序清单 8-11 中的 SetTest 程序会将 Item 对象插入到一个散列集中。当你用修改过的类文件来运行该程序时,会看到下面的日志记录信息:

```
May 17, 2016 10:57:59 AM Item hashCode
FINER: ENTRY
May 17, 2016 10:57:59 AM Item hashCode
FINER: ENTRY
May 17, 2016 10:57:59 AM Item hashCode
FINER: ENTRY
May 17, 2016 10:57:59 AM Item equals
FINER: ENTRY
[description=Toaster, partNumber=1729], [description=Microwave, partNumber=4104]]
```

当将同一项插入两次时, 请注意对 equals 的调用。

这个示例显示了字节码工程的强大之处:注解可以用来向程序中添加一些指示,而字节码编辑工具则可以提取这些指示,然后修改虚拟机指令。

#### 程序清单 8-9 bytecodeAnnotations/EntryLogger.java

```
package bytecodeAnnotations;
2
3 import java.jo.*;
4 import java.nio.file.*;
  import org.objectweb.asm.*;
  import org.objectweb.asm.commons.*;
7
R
9
   * Adds "entering" logs to all methods of a class that have the LogEntry annotation.
10
    * @version 1.21 2018-05-01
11
    * @author Cay Horstmann
12
    */
13
   public class EntryLogger extends ClassVisitor
14
15
      private String className;
16
17
      /**
18
       * Constructs an EntryLogger that inserts logging into annotated methods of a given class.
19
28
      public EntryLogger(ClassWriter writer, String className)
21
22
23
         super(Opcodes.ASM5, writer);
         this.className = className;
24
25
26
      public MethodVisitor visitMethod(int access, String methodName, String desc,
27
            String signature, String[] exceptions)
28
29
         MethodVisitor mv = cv.visitMethod(access, methodName, desc, signature, exceptions);
30
         return new AdviceAdapter(Opcodes.ASM5, mv, access, methodName, desc)
31
32
            private String loggerName;
33
34
            public AnnotationVisitor visitAnnotation(String desc, boolean visible)
35
```

```
{
36
                return new AnnotationVisitor(Opcodes.ASM5)
37
38
                      public void visit(String name, Object value)
39
48
                         if (desc.equals("LbytecodeAnnotations/LogEntry;")
41
                                && name.equals("logger"))
42
                            loggerName = value.toString();
43
44
                   };
45
             }
46
47
             public void onMethodEnter()
48
49
                if (loggerName != null)
50
                {
51
                   visitLdcInsn(loggerName);
52
                   visitMethodInsn(INVOKESTATIC, "java/util/logging/Logger", "getLogger",
53
                      "(Ljava/lang/String;)Ljava/util/logging/Logger;", false);
54
                   visitLdcInsn(className);
55
                   visitLdcInsn(methodName);
56
                   visitMethodInsn(INVOKEVIRTUAL, "java/util/logging/Logger", "entering",
57
                       "(Ljava/lang/String;Ljava/lang/String;)V", false);
58
                   loggerName = null;
59
                }
60
             }
61
          };
62
       }
63
64
       /**
65
        * Adds entry logging code to the given class.
66
        * @param args the name of the class file to patch
67
        */
68
       public static void main(String[] args) throws IOException
69
78
          if (args.length == 0)
71
72
             System.out.println("USAGE: java bytecodeAnnotations.EntryLogger classfile");
73
             System.exit(1);
74
75
          Path path = Path.of(args[0]);
76
          var reader = new ClassReader(Files.newInputStream(path));
77
          var writer = new ClassWriter(
78
             ClassWriter.COMPUTE MAXS | ClassWriter.COMPUTE FRAMES);
79
          var entryLogger = new EntryLogger(writer,
RA
             path.toString().replace(".class", "").replaceAll("[/\\\]", "."));
81
          reader.accept(entryLogger, ClassReader.EXPAND FRAMES);
82
          Files.write(Path.of(args[0]), writer.toByteArray());
 83
84
       }
   }
 85
```

```
2
3 import java.util.*;
   import bytecodeAnnotations.*;
5
6
    * An item with a description and a part number.
    * @version 1.01 2012-01-26
    * @author Cay Horstmann
    */
10
   public class Item
11
   {
12
      private String description;
13
      private int partNumber;
14
15
      /**
16
       * Constructs an item.
17
       * @param aDescription the item's description
18
       * @param aPartNumber the item's part number
19
20
      public Item(String aDescription, int aPartNumber)
21
      {
22
         description = aDescription;
23
24
         partNumber = aPartNumber;
25
26
27
       * Gets the description of this item.
28
       * @return the description
29
38
      public String getDescription()
31
32
33
         return description;
34
35
      public String toString()
36
37
         return "[description=" + description + ", partNumber=" + partNumber + "]";
38
39
48
      @LogEntry(logger = "com.horstmann")
41
      public boolean equals(Object otherObject)
42
43
44
         if (this == otherObject) return true;
         if (otherObject == null) return false;
45
45
          if (getClass() != otherObject.getClass()) return false;
          var other = (Item) otherObject;
47
          return Objects.equals(description, other.description) && partNumber == other.partNumber;
48
49
50
      @LogEntry(logger = "com.horstmann")
51
      public int hashCode()
52
53
          return Objects.hash(description, partNumber);
54
55
   }
56
```

#### 程序清单 8-11 set/SetTest.java

```
1 package set;
2
3 import java.util.*;
4 import java.util.logging.*;
6
    * @version 1.03 2018-05-01
    * @author Cay Horstmann
9
   public class SetTest
10
   {
11
      public static void main(String[] args)
12
13
         Logger.getLogger("com.horstmann").setLevel(Level.FINEST);
14
         var handler = new ConsoleHandler();
15
         handler.setLevel(Level.FINEST);
16
         Logger.getLogger("com.horstmann").addHandler(handler);
17
18
         var parts = new HashSet<Item>();
19
         parts.add(new Item("Toaster", 1279));
28
         parts.add(new Item("Microwave", 4104));
21
         parts.add(new Item("Toaster", 1279));
22
         System.out.println(parts);
23
      1
24
25 }
```

#### 8.7.2 在加载时修改字节码

在前一节中,已经看到了一个用于编辑类文件的工具。但是,在把另一个工具添加到程序的构建过程中时,会显得笨重不堪。更吸引人的做法是将字节码工程延迟到载入时,即类加载器加载类的时候。

设备(instrumentation)API 提供了一个安装字节码转换器的挂钩。不过,必须在程序的 main 方法调用之前安装这个转换器。通过定义一个代理,即被加载用来按照某种方式监视程序的一个类库,就可以处理这个需求。代理代码可以在 premain 方法中执行初始化。

下面是构建一个代理所需的步骤:

1. 实现一个具有下面这个方法的类:

public static void premain(String arg, Instrumentation instr)

当加载代理时,此方法会被调用。代理可以获取一个单一的命令行参数,该参数是通过 arg 参数传递进来的。instr 参数可以用来安装各种各样的挂钩。

2. 制作一个清单文件 EntryLoggingAgent.mf 来设置 Premain-Class 属性。例如:

Premain-Class: bytecodeAnnotations.EntryLoggingAgent

3. 将代理代码打包, 并生成一个 JAR 文件, 例如:

```
\label{lem:condense} javac \ -classpath \ .: asm/\* bytecodeAnnotations/EntryLoggingAgent.java \\ jar \ cvfm \ EntryLoggingAgent.jar \ bytecodeAnnotations/EntryLoggingAgent.mf \ \ bytecodeAnnotations/Entry*.class
```

为了运行一个具有该代理的 Java 程序,需要使用下面这个命令行选项:

java -javaagent: AgentJARFile=agentArgument . . .

例如,运行具有日志代理的 SetTest 程序需调用:

```
javac set/SetTest.java
java -javaagent:EntryLoggingAgent.jar=set.Item -classpath .:asm/\* set.SetTest
```

Item参数是代理应该修改的类的名称。

程序清单 8-12 展示了这个代理的代码。该代理安装了一个类文件转换器,这个转换器首先检验类名是否与代理参数相匹配。如果匹配,那么它会利用上一节那个 EntryLogger 类修改字节码。不过,修改过的字节码并不保存成文件。相反,转换器会将它们返回,以加载到虚拟机中(参见图 8-3)。换句话说,这项技术实现的是"即时"(just in time)字节码修改。

#### 程序清单 8-12 bytecodeAnnotations/EntryLoggingAgent.java

```
package bytecodeAnnotations;
2
  import java.lang.instrument.*;
3
   import org.objectweb.asm.*;
6
   /**
7
    * @version 1.11 2018-05-01
    * @author Cay Horstmann
9
10
   public class EntryLoggingAgent
11
   {
12
      public static void premain(final String arg, Instrumentation instr)
13
14
         instr.addTransformer(new ClassFileTransformer()
15
16
               public byte[] transform(ClassLoader loader, String className, Class<?> cl,
17
                      ProtectionDomain pd, byte[] data) throws IllegalClassFormatException
18
19
                   if (!className.replace("/", ".").equals(arg)) return null;
28
                   var reader = new ClassReader(data);
21
                   var writer = new ClassWriter(
22
                      ClassWriter.COMPUTE MAXS | ClassWriter.COMPUTE FRAMES);
23
                   var el = new EntryLogger(writer, className);
24
                   reader.accept(el, ClassReader.EXPAND FRAMES);
25
                   return writer.toByteArray();
26
27
            });
28
      }
29
   }
38
```

![](_page_187_Figure_2.jpeg)

图 8-3 在加载时修改类

在本章, 你已经学习到了以下的知识:

- 怎样向 Java 程序中添加注解。
- 怎样设计你自己的注解接口。
- 怎样实现可以利用注解的工具。

你已经看到了三种处理代码的技术:编写脚本、编译 Java 程序和处理注解。前两种技术十分简单。而另一方面,构建注解工具可能会很复杂,但这并非是大多数开发者都需要解决的问题。本章向你介绍了一些背景知识,有助于你去理解可能会碰到的注解工具内部工作机制,但这些背景知识可能会挫伤你自行开发工具的积极性。

下一章将讨论 Java 平台模块系统,它是 Java 9 的关键特性,是促进 Java 平台向前发展的重要动力。

## *9 Java平台模块*

- *模块 概念*
- *对模块命名*
- *模块化 "Hello, World !" <sup>序</sup>*
- *对模块 求*
- *导出包*
- *模块化 JAR*
- *模块和反射式*

- *动模块*
- *不具名模块*
- *于 命令 标*
- *传 求和 态 求*
- *定导出和开放*
- *服务加*
- *操作模块 工具*

*封 是 向对 一个 性。类的声明 公有接口和 有实 构成 可以 只修改实 不影响其 户 方式 得以演化。模块 为 带来了大 同 处。 模块使 和包可以有 择性地 取 从 使得模块 演化可以受控。*

*多个 有 Java模块 依 于 加 器来实 之 。但是 Java 9引人 了一个 Java 器和 拟机支持 新 为Java平台模块 。它 来模块 化基于Java平台 大型代 基。如果愿意 也可以使 个 来模块化我们 己 应 序。*

*无 是否在 己 应 序中使 Java平台模块 你 可 会受到模块化 Java平台 影响。本 将展 如何声明和使 Java平台模块。你 会学习到如何 你 应 序 使其 够与模块化 Java平台和 三方模块一 工作。*

## *9.1模块 概念*

*在 向对象编程中 基础的构建要素就是 。 提供了封 有 性只能被具有明 权 代 即 只 其所属 中 方法 使得对 情况 推断成为可 。如果某个 有变 发 了变化 么我们就会发 一 列可 出 方法。如果需要修 改 有表示 么就 哪些方法会受到影响。*

*在Java中 包提供了更 一 方式 包是 合。包也提供了一 封 别, 具有包 权 所有 性 无 是公有 是 有 只 同一个包中 方法 。*

*但是 在大型 中 别 控制仍显不 。所有公有 性 即在包 外 也 可以访问的特性 可以从任何地方 。假 我们想 修改或剔 一个很少使 性 如 果它是公有 么就没有办法推断 个变化所产 影响。*

*Java平台 们 对 就是 情况。 去20年中 JDK呈 式发展 但是有*

些特性现在明显过时了。有一个大家都喜欢提到的例子,即 CORBA。你最后一次使用它是什么时候?但是 org.omg.corba 包仍旧打包在每一个 JDK 中,直至 Java 10。到了 Java 11,仍旧需要这个包的那些极少数的人就必须将所需的 JAR 文件自己添加到他们的项目中了。

java.awt 的情况又如何呢? 服务器端的应用程序并不需要它,对吗? 但是, java.awt. DataFlavor 类在 SOAP 的实现中仍在使用,这是一种基于 XML 的 Web 服务协议。

Java 平台的设计者们在面对规模超大且盘根错节的代码时,认为他们需要一种能够提供更多控制能力的构建机制。他们研究了现有的模块系统(例如 OSGi),发现它们都不适用于他们的问题。于是,他们设计了一个新的系统,称为 Java 平台模块系统,现在成了 Java 语言和虚拟机的一部分。这个系统已经成功地用于 Java API 的模块化,如果愿意,也可以使用这个系统来模块化我们自己的应用程序。

- 一个 Java 平台模块包含:
- 一个包集合
- 可选地包含资源文件和像本地库这样的其他文件
- 一个有关模块中可访问的包的列表
- 一个有关这个模块依赖的所有其他模块的列表

Java 平台在编译时和在虚拟机中都强制执行封装和依赖。

为什么在我们自己的程序中要考虑使用 Java 平台模块系统而不是传统的使用类路径上的 JAR 文件呢? 因为这样做有以下两个优点。

- 1. 强封装: 我们可以控制哪些包是可访问的,并且无须操心去维护那些我们不想开放给公众去访问的代码。
  - 2. 可靠的配置: 我们可以避免诸如类重复或丢失这类常见的类路径问题。

还有一些有关 Java 平台模块系统的话题我们没有涉及,例如模块的版本管理。当前还不支持指定要求使用模块的具体版本,或者在同一个程序中使用某个模块的多个版本。这些特性可能正是人们所期望的,但是如果需要用到它们,就必须使用 Java 平台模块系统之外的机制。

#### 9.2 对模块命名

模块是包的集合。模块中的包名无须彼此相关。例如,java.sql 模块中就包含了 java.sql、javax.sql 和 javax.transaction.xa 这几个包。并且,正如这个例子所示,模块名和包名相同是完全可行的。

就像路径名一样,模块名是由字母、数字、下划线和句点构成的。而且,和路径名一样,模块之间没有任何层次关系。如果有一个模块是 com. horstmann, 另一个模块是 com. horstmann.corejava, 那么就模块系统而言,它们是无关的。

当创建供他人使用的模块时,重要的是要确保它的名字是全局唯一的。我们期望大多数的模块名都遵循"反向域名"惯例,就像包名一样。

命名模块最简单的方式就是按照模块提供的顶级包来命名。例如,SLF4J 日志记录外观有一个 org.slf4j 模块,其中包含的包为 org.slf4j、org.slf4j.spi、org.slf4j.event 和 org.slf4j.helpers。

这个惯例可以防止模块中产生包名冲突,因为任何给定的包都只能被放到一个模块中。如果模块名是唯一的,并且包名以模块名开头,那么包名也就是唯一的。

我们可以使用更短的模块名来命名不打算给其他程序员使用的模块,例如包含某个应用程序的模块。只是为了展示这样做可行,本章就使用了这种方式,那些貌似应该成为库代码的模块都具有像 com.horstmann.util 这样的名字,而包含程序(其中有一个带有 main 方法的类)的模块都具有像 v2ch09.hellomod 这样很容易记忆的名字。

直 注释:模块名只用于模块声明中。在Java类的源文件中,永远都不应该引用模块名,而是应该按照一如既往的方式去使用包名。

#### 9.3 模块化的 "Hello, World!" 程序

让我们把传统的"Hello, World!"程序转换为一个模块。首先,我们需要将这个类放到一个包中,"不具名的"包是不能包含在模块中的。下面是代码:

```
package com.horstmann.hello;

public class HelloWorld
{
    public static void main(String[] args)
    {
        System.out.println("Hello, Modular World!");
    }
}
```

到目前为止,还没有任何东西有变化。为了创建包含这个包的 v2ch09.hellomod 模块,需要添加一个模块声明,可以将其置于名为 module-info.java 的文件中,该文件位于基目录中(即,包含 com 目录的目录)。按照惯例,基目录的名字与模块名相同。

```
v2ch09.hellomod/
L module-info.java
com/
L horstmann/
L hello/
L HelloWorld.java
module-info.java 文件包含模块声明:
module v2ch09.hellomod
{
}
```

这个模块声明之所以为空,是因为该模块没有任何可以向其他人提供的内容,它也不需要依赖任何东西。

现在,按照往常一样编译它:

*javac v2ch89.heUoiMJd/module-info java v2ch99. hellomod/com/horstmann/heUo/HelloWorid java*

*module-info, java 个文件 来与Java源文件不同 当然 不可 存在名为module-info 因为 名不 包含 <sup>字</sup> 。<sup>关</sup> <sup>同</sup>module和在下一 将会 <sup>到</sup> requires, exports <sup>关</sup> 是" 定关键词" 即只在模块声明中具有 殊含义。 个文件会以二 制形式 到包含 模块定义 文件module-info.class中。*

*为了 个 序作为模块化应 序来 指定模块 径 它与类路径 似 但 是包含 是模块。 以模块名/ 名 形式指定主*

*java -module-path v2ch09.heUomod -module v2ch69.heUomod/coni.horstmann.hello.HelloWorld*

*也可以不使 --module-path和-module, 是使 单字母 -p和-m*

*java -p v2che9.heUomod v2ch09.heUomod/com.horstmann.hello.HeUoWorld*

*<sup>无</sup> <sup>哪</sup> 方式 会显 <sup>候</sup> "HeUo, Module World!", 明我们成功地模块化了 一个 应 序。*

## *<sup>Q</sup> <sup>注</sup> <sup>在</sup> 个模块时 <sup>会</sup> 得一条 告消息*

*warning:【module] module name component v2chG9 should avoid terminal digits*

*条 告意在建 序员不 模块名添加 本号。你可以忽 个 告 或 注 来抑制它*

```
@SuppressWarnings(•module0)
module v2ch .heUomod
{
}
```

*在 一点上 module声明就像 声明一样 可以对其 注 。(注 型必 具有值为 ElementType.MODULE target )*

## *9.4对模块 <sup>求</sup>*

*我们创建一个新 模块v2ch 9. equiremod,其中使 一个JOptionPane对 展 了消息 " Hello, Modular World ! "*

```
package con.horstmann.hello;
import j avax.swing.JOptionPane:
public class HelloWorld
{
   public static void main(String[] args)
   {
      JOptionPane.showMessageDialog(null, "Hello, Modular World!");
   }
}
```

*在 会失 并报下 消息*

error: package javax.swing is not visible (package javax.swing is declared in module java.desktop, but module v2ch09.requiremod does not read it)

JDK 已经被模块化了,并且 javax.swing 包现在包含在 java.desktop 模块中。我们的模块需要声明它依赖于这个模块:

```
module v2ch09.requiremod
{
   requires java.desktop;
}
```

模块系统的设计目标之一就是模块需要明确它们的需求, 使虚拟机可以确保在启动程序 之前所有的需求都得以满足。

在前一节中,并没有产生明确的需求,因为我们只用到了 java.lang 和 java.io 包。这些包都包含在默认需要的 java.base 模块中。

注意,我们的 v2ch09.requiremod 模块只列出了它自己的模块需求。它需要 java.desktop 模块,这样它才能使用 javax.swing 包。java.desktop 模块自身声明了它需要其他三个包,即 java.

datatransfer、java.prefs 和 java.xml。

图 9-1 展示了一张模块图,图中的节点是模块,而图中的边,也就是连接节点的箭头,要么声明了需求,要么在没有声明任何需求时表示需要 java.base。

在模块图中不能有环,即,一个模块 不能直接或间接地对自己产生依赖。

模块不会自动地将访问权限传递给其他模块。在我们的示例中,java.desktop模块声明它需要 java.prefs,而 java.prefs模块声明它需要 java.xml,但是这并不会赋予 java.desktop使用来自 java.xml 模块中的包的权力。按照数学术语描述,require不是"传递性"的。通常,这种行为正是我们想要的,因为它使得需求必须明确化,

![](_page_192_Figure_12.jpeg)

图 9-1 Swing 应用程序 "Hello, Modular World!" 的模块图

但是正如你将会在9.11节中看到的,在某些情况下,可以放松这条限制。

- i 注释: 本节开头部分给出的错误消息声明我们的 v2ch99.requiremod 模块没有"读入" java.desktop 模块。按照 Java 模块系统的用语,模块 M 会在下列情况下读入模块 N:
  - 1. M 需要 N
    - 2. M需要某个模块,而该模块传递性地需要 N (参阅 9.11 节)
    - 3. N 是 M 或 java.base

#### 9.5 导出包

在前一节中,我们看到一个模块如果想要使用其他模块中的包,就必须声明需要该模块。但是,这并不会自动使得所需模块中所有的包都可用。模块可以用 exports 关键词来声明它的哪些包可用。例如,下面是 java.xml 模块的模块声明中的一部分:

```
module java.xml
{
    exports javax.xml;
    exports javax.xml.catalog;
    exports javax.xml.datatype;
    exports javax.xml.namespace;
    exports javax.xml.parsers;
    . . .
}
```

这个模块让许多包都可用,但是通过不导出其他的包而隐藏了它们(例如 jdk.xml.internal)。 当包被导出时,它的 public 和 protected 的类和接口,以及 public 和 protected 的成员,在模块的外部也是可以访问的(如往常一样,protected 的类型和成员只有在子类中才是可访问的)。

但是,没有导出的包在其自己的模块之外是不可访问的,这与 Java 模块化之前很不相同。在过去,我们可以使用任何包中公有的类,尽管它可能并非公有 API 的一部分。例如,当公有 API 没有提供相对应的适合的功能时,通常会推荐使用像 sun.misc.BASE64Encoder 或 com. sun.rowset.CachedRowSetImpl 这样的类。

现在,不能再访问 Java 平台 API 中未导出的包了,因为所有的这些包都包含在模块的内部。因此,有些程序不能再用 Java 9 来运行了。当然,从来没有人承诺过会让非公有的 API 一直保持可用,因此大家不应该对此感到震惊。

让我们在一个简单场景中使用导出机制。我们将准备一个 com.horstmann.greet 模块,它会导出一个名字也是 com.horstmann.greet 的包,这遵循了向他人提供代码的模块应该按照其内部的顶层包来命名的惯例。还有一个名为 com.horstmann.greet.internal 的包,我们并不会导出它。

公有的 Greeter 接口在第一个包中。

```
public interface Greeter
{
    static Greeter newInstance()
    {
        return new com.horstmann.greet.internal.GreeterImpl();
    }
    String greet(String subject);
}

第二个包有一个实现了该接口的类。这个类是公有的,因为它需要在第一个包中是可访问的:
package com.horstmann.greet.internal;\nimport com.horstmann.greet.Greeter;
```

```
public class GreeterImpl implements Greeter
  public String greet(String subject)
     return "Hello, " + subject + "!";
com.horstmann.greet 模块包含这两个包, 但是只会导出第一个包:
module com.horstmann.greet
{
   exports com.horstmann.greet;
}
第二个包在模块外部是不可访问的。
我们将应用程序放到第二个包中,它需要用到第一
module v2ch09.exportedpkg
{
   requires com.horstmann.greet;
注释: exports 语句后面跟着包名,而 requires 语句后面跟着模块名。
现在,我们的应用程序将使用 Greeter 来获取问候语:
package com.horstmann.hello;
import com.horstmann.greet.Greeter;
public class HelloWorld
   public static void main(String[] args)
     Greeter greeter = Greeter.newInstance();
     System.out.println(greeter.greet("Modular World"));
}
下面是这两个模块的源文件结构:
com.horstmann.greet
 - module-info.java
  com
  L horstmann
    L greet
      Greeter.java
      internal
       GreeterImpl.java
v2ch09.exportedpkg
  module-info.java
  com
  L horstmann
   L hello
     L HelloWorld. java
```

*为了构建 个应用程序 先要编译com.horstmann.greet模块*

*javac con.horstmann.greet/module-info.java \ com.horstmann.greet/com/horstmann/greet/Greeter.java \ com. horstmann.greet/com/horstmann/greet/internal/Greeterlrnpl. java*

*然后 模块 径上 一个模块来 个应 序模块*

*javac -p com.horstmann.greet v2ch09.exportedpkg/module-info.java \ v2ch99 • exportedpkg/coiR/horst«ann/heUo/HeUoWorld .java*

*最后 模块 径上 两个模块来 个 序*

*java -p v2ch69.exportedpkg:com.horstmann.greet \ •m v2ch69.exportedpkg/com.horstmann.hello.HelloWorld*

*提 如果要用Eclipse来构建 个应 序 为每一个模块建 一个单 工 。在v2ch09.exportedpkg项目中 编辑项目属性。在Projects 上 添加com. horstmann.greet模块到模块 径中 参 图9-2。*

![](_page_195_Picture_9.jpeg)

*图9-2添加依 模块到Eclipse项目中*

*在 你已 到了构成Java平台模块系统基础的requires和exports 句。正如你所 模块 在概念上很 单。模块指定了它们需要哪些模块 以及它们可以向其他模块提 供哪些包。9.12 将展 exports 句 一个次 变体。*

*0 <sup>告</sup> 模块没有作 <sup>域</sup> 概念。<sup>不</sup> 在不同 模块中放 两个具有 同名字 <sup>包</sup>。<sup>即</sup> 使是 包 即不会导出 包 情况也是如此。*

#### 9.6 模块化的 JAR

到目前为止,我们直接将模块编译到了源代码的目录树中。很明显,这无法满足部署的要求。模块可以通过将其所有的类都置于一个 JAR 文件中而得以部署,其中 module-info.class 在 JAR 文件的根部。这样的 JAR 文件被称为模块的 JAR。

要想创建模块化的 JAR 文件,只需以通常的方式使用 jar 工具。如果有多个包,那么最好是用-d 选项来编译,这样可以将类文件置于单独的目录中,如果该目录不存在,则会创建该目录。然后,在收集这些类文件时使用-c 选项的 jar 命令来修改该目录。

javac -d modules/com.horstmann.greet \$(find com.horstmann.greet -name \*.java)
jar -c -v -f com.horstmann.greet.jar -C modules/com.horstmann.greet .

如果你使用的是像 Maven、Ant 或 Gradle 这样的构建工具,那么只需按照你惯用的方式来构建 JAR 文件。只要 module-info.class 包含在内,就可以得到该模块的 JAR 文件。

然后,在模块路径中包含该模块化的 JAR,该模块就会被加载。

● 警告: 在过去,包中的类有时会分布在多个 JAR 文件中。(这种包被称为"分离包"。) 这可能从来就不是一个好注意,对于模块来说也不可能是个好主意。

就像常规的 JAR 文件一样,可以指定模块化的 JAR 中的主类:

javac -p com.horstmann.greet.jar \
 -d modules/v2ch09.exportedpkg \$(find v2ch09.exportedpkg -name \*.java)
jar -c -v -f v2ch09.exportedpkg.jar -e com.horstmann.hello.HelloWorld \
 -C modules/v2ch09.exportedpkg .

当启动该程序时,可以指定包含主类的模块:

java -p com.horstmann.greet.jar:v2ch09.exportedpkg.jar -m v2ch09.exportedpkg

在创建 JAR 文件时,可以选择指定版本号。使用 --module-version 选项,以及在 JAR 文件名上添加 @ 和版本号:

 $\texttt{jar-c-v-f} \ \ \textbf{com.horstmann.greet@1.0.jar--module-version 1.0-C} \ \ \texttt{com.horstmann.greet} \ \ .$ 

正如已经讨论过的, Java 平台模块系统并不会使用版本号来解析模块, 但是可以通过其他工具和框架来查询版本号。

**注释:** 可以通过反射 API 找到版本号。在我们的示例中:
Optional<String> version = Greeter.class.getModule().getDescriptor().rawVersion();
将产生一个包含版本号字符串 "1.0" 的 Optional。

這程:等价于类加载器的模块是一个层。Java 平台模块系统会将 JDK 模块和应用程序模块加载到启动层 (boot layer)。程序还可以使用分层 API 加载其他模块 (本书不会讨论该 API)。这种程序可以选择考虑模块的版本。Java 期望像 Java EE 应用服务器这样的程序的开发者会利用分层 API 来提供对模块的支持。

√ 提示: 如果想要加载模块到 JShell 中, 需要将 JAR 包含在模块路径中, 并使用 --addmodules 选项:

jshell --module-path com.horstmann.greet@1.0.jar --add-modules com.horstmann.greet

#### 9.7 模块和反射式访问

在前面的章节中,我们看到了模块系统是如何强制执行封装的。模块只能访问显式地由 其他包导出的包。在过去,总是可以通过使用反射来克服令人讨厌的访问权限问题。正如在 卷 I 第 5 章中看到的,反射可以访问任何类的私有成员。

但是,在模块化的世界中,这条路再也行不通了。如果一个类在某个模块中,那么对非 公有成员的反射式访问将失败。特别是,回忆一下我们是如何访问私有域的:

```
Field f = obj.getClass().getDeclaredField("salary");
f.setAccessible(true);
double value = f.getDouble(obj);
f.setDouble(obj, value * 1.1);
```

f.setAccessible(true)调用会成功,除非安全管理器不允许对私有域的访问。但是,使用安全管理器来运行 Java 应用程序并不常见,并且有许多使用反射式访问的库。典型的例子包括像 JPA 这样的对象 – 关系映射器,它们会自动地将对象持久化到数据库中,以及在对象和 XML 或 JSON 之间转换的库中,例如 JAXB 和 JSON-B。

如果使用这种库,并且还想使用模块,那么就必须格外小心。为了演示这个问题,让我们将卷 I 第 5 章中的 0bjectAnalyzer 类放到 com.horstmann.util 模块中。这个类有一个 toString 方法,可以使用反射机制来打印出对象的域。

单独的 v2ch09.openpkg 模块包含一个简单的 Country 类:

```
public class Country
{
    private String name;
    private double area;

    public Country(String name, double area)
    {
        this.name = name;
        this.area = area;
    }
    // . . .
}

下面的短程序演示了如何分析 Country 对象:
package com.horstmann.places;\nimport com.horstmann.util.*;
```

```
public class Demo
   public static void main(String[] args) throws ReflectiveOperationException
      var belgium = new Country("Belgium", 30510);
      var analyzer = new ObjectAnalyzer();
      System.out.println(analyzer.toString(belgium));
现在编译模块和 Demo 程序:
javac com.horstmann.util/module-info.java \
   com.horstmann.util/com/horstmann/util/ObjectAnalyzer.java
javac -p com.horstmann.util v2ch09.openpkg/module-info.java \
   v2ch09.openpkg/com/horstmann/places/*.java
java -p v2ch09.openpkg:com.horstmann.util -m v2ch09.openpkg/com.horstmann.places.Demo
该程序会以下面的异常而失败:
Exception in thread "main" java.lang.reflect.InaccessibleObjectException:
   Unable to make field private java.lang.String com.horstmann.places.Country.name
   accessible: module v2ch09.openpkg does not "opens com.horstmann.places" to module
   com.horstmann.util
```

当然,按照纯理论来说,破坏对象的封装并窥视其私有成员是错误的。但是像对象 - 关系映射或 XML/JSON 绑定这样的机制应用非常广泛,使得模块系统必须接纳它们。

通过使用 opens 关键词,模块就可以打开包,从而启动对给定包中的类的所有实例进行反射式访问。下面是我们的模块必须执行的操作:

```
module v2ch09.openpkg
{
    requires com.horstmann.util;
    opens com.horstmann.places;
}

有了这样的变化,ObjectAnalyzer 就可以正确地工作了。
模块可以像下面这样声明为 Open (开放的):
    open module v2ch09.openpkg
{
        requires com.horstmann.util;
}
```

开放的模块可以授权对其所有包的运行时访问,就像所有的包都用 exports 和 opens 声明过一样。但是,在运行时只有显式导出的包是可访问的。开放模块将模块系统编译时的安全性和经典的授权许可的运行时行为结合在一起。

回忆一下卷 I 第 5 章, JAR 文件除了类文件和清单外,还可以包含文件资源,它们可以被 Class.getResourceAsStream 方法加载,现在还可以被 Module.getResourceAsStream 加载。如果资源存储在匹配模块的某个包的目录中,那么这个包必须对调用者是开放的。在其他目录中的资源,以及类文件和清单,可以被任何人读取。

宣 注释: 作为更贴近实际的例子, 按照 JSON-B 规范, 我们把 Country 对象转换为 XML 或 JSON。

为了使用 JSON-B 的 Yasson 实现, 需要从 Maven Central Repository 中下载 Jakata. jason-api-2.0.1.jar、Jakarta.json.bind-api-2.0.0.jar、Jakarta.json-2.0.1-module.jar 和 yasson-2.0.3.jar。将这些 JAR 文件放到模块路径上, 然后运行 com.horstmann.places.Demo2程序, 当 com.horstmann.places 包开放时, 向 JSON 的转换就会成功。

**注释**:未来的库可能会使用**变量句柄**而不是反射来读写域。VarHandle 类似于 Field。我们可以使用它来读写指定类的任何实例的指定域。但是,为了获得 VarHandle 对象,库代码需要一个 Lookup 对象:

```
public Object getFieldValue(Object obj, String fieldName, Lookup lookup)
```

只要该模块中生成的 Lookup 对象拥有对该域的访问权,这段代码就可以工作。在模块中的某些方法可以直接调用 MethodHandles.lookup(),它会产生一个封装了调用者访问权限的对象。在这种方式下,一个模块可以赋予另一个模块访问私有成员的权限。在实践中,需要解决如何以麻烦最少的方式赋予这些权限的问题。

#### 9.8 自动模块

现在你知道了如何使用 Java 平台模块系统。如果从全新的项目开始,其中所有的代码都由我们自己编写,那么就可以设计模块、声明模块依赖关系,并将应用程序打包成模块化的 JAR 文件。

但是,这是一种非常罕见的场景,几乎所有的项目都依赖于第三方的库。当然,我们可以等到所有库的提供商都将库演化成模块,然后再模块化我们自己的代码。

但是如果等不及怎么办呢? Java 平台模块系统提供了两种机制来填补将当今的前模块化世界与完全模块化应用程序割裂开来的鸿沟:自动化模块和不具名模块。

如果是为了迁移,我们可以通过把任何 JAR 文件置于模块路径的目录而不是类路径的目录中,实现将其转换成一个模块。模块路径上没有 module-info.class 文件的 JAR 被称为自动模块。自动模块具有下面的属性:

- 1. 模块隐式地包含对其他所有模块的 requires 子句。
- 2. 其所有包都被导出,且是开放的。

- *3. 如果在JAR文件清单META-INF/MANIFEST.MF中具有 为Automatic-Module-Name 么 它 值会变为模块名。*
- *4. 否则 模块名将从JAR文件文件名中 得 将文件名中尾 本号删 并将 字 母数字 字 替换为句点。*

*前两条 则 明 动模块中 包 为和在 径上一样。使 模块 径 原因是为了 其他模块受 使得它们可以 对 个模块 依 关 。*

*例如 假 我们正在实 一个处 CSV文件 模块 并使 了 Apache Commons CSV <sup>库</sup>o我们想 <sup>在</sup>module-info, java文件中 模块 <sup>依</sup> Apache Commons CSV。*

*如果在模块 径中添加co )ns-csv-1.9.e.jar 么我们 模块就可以引 个模块 了。它 名字是co ns.csv,因为去掉了尾部版本号-1.9.0, 字母数字字 替换成了 句点。*

*个名字也 是一个可接受 模块名 因为Commons CSV人们 其他人也 不太可 会 个名字来命名其他 模块。但是 如果 个JAR文件 护 同意保 反向 域名 使 更好 包名org.apache.commons.csv作为模块名 会显得更好。他们只 在 JAR 中 META-INF/MANIFEST.MF 文件 添加一*

*Automatic-Module.Name: org.apache.commons.csv*

*最 我们期望他们 够在module-info, java中添加保 模块名将 个JAR文件 换成 一个 正 模块 每个 模块名引 了 个CSV模块 模块也 够 工作。*

*注 模块 划是一 伟大 会实 没有人 它是否 够 利实施。在 将 三方 JAR放到模块 径之前 检查它们是否是模块化 。如果不是 它们 清单是否有模块名 如果没有 仍旧 将 样 JAR 换成 动模块 但是 准 备妤以后更新 模块名。*

*在撰写本书时 Commons CSV JAR文件 1.9.0 本 没有模块描 或 动模块名。 尽 如此 它在模块 径上工作 好。我们可以从https://commons.apache.org/proper/conrnons-csv 处下载这个库 压并将commons-csv.1.9.6.jar放到v2che9.automod模块 录中。 个模块包 含了一个很 单 从CSV文件中 取国家数据 序*

```
package com.horstmann.places;
import java.io.*;
import org.apache.commons.csv. ;
public class CSVDemo
{
   public static void main(String[] args) throws IOException
   {
      var in = new FileReader("countries.csv");
      Iterable<CSVRecord> records = CSVFormat.EXCEL.withDelimiter(';')
            .withHeader().parse(in);
      for (CSVRecord record : records)
```

```
{
        String name = record.get("Name");
        double area = Double.parseDouble(record.get("Area"));
        System.out.println(name + " has area " + area);
  }
}
因为我们将 commons-csv-1.9.0.jar 用作自动模块, 所以我们要声明需要它:
@SuppressWarnings("module")
module v2ch09.automod
   requires commons.csv:
下面是编译和运行该程序的命令:
javac -p v2ch09.automod:commons-csv-1.9.0.jar \
   v2ch09.automod/com/horstmann/places/CSVDemo.java \
   v2ch09.automod/module-info.java
java -p v2ch09.automod:commons-csv-1.9.0.jar \
   -m v2ch09.automod/com.horstmann.places.CSVDemo
```

#### 9.9 不具名模块

任何不在模块路径中的类都是不具名模块的一部分。从技术上说,可能会有多个不具名 模块,但是它们合起来看就像是单个不具名的模块。与自动模块一样,不具名模块可以访问 所有其他的模块,它的所有包都会被导出,并且都是开放的。

但是,没有任何明确模块可以访问不具名的模块。(明确模块是指既不是自动模块也不是不具名模块的模块,即,module-info.class 在模块路径上的模块。)换句话说,明确模块总是可以避免"类路径的坑"。

例如,考虑前一节的程序,假设将 commons-csv.1.9.0.jar 放到类路径而不是模块路径上:

```
java --module-path v2ch09.automod \
    --class-path commons-csv-1.9.0.jar \
    -m v2ch09.automod/com.horstmann.places.CSVDemo
```

#### 现在,这个程序将无法启动:

Error occurred during initialization of boot layer java.lang.module.FindException: Module commons.csv not found, required by v2ch09.automod

因此,迁移到 Java 平台模块系统必须按照自底向上的方式处理:

- 1. Java 平台自身被模块化。
- 2. 接下来,库被模块化,要么通过使用自动模块,要么将它们转换为明确模块。
- 3. 一旦应用程序使用的所有库都被模块化,就可以将应用程序的代码转换为一个模块。

**注释**:自动模块可以读取不具名模块,因此它们的依赖关系放在类路径中。

### *9.10 <sup>于</sup> 命令 <sup>标</sup>*

*即使我们 序没有使 模块 在使 Java 9或更新 本时 我们也无法 模块化 世 。即使应 序 代 位于不具名模块 径上 并且所有 包 导出且开放 它也 与模块化 Java平台交互。*

*到了 Java 11, 时封 是严格强制执 。但是 在Java 16之前 时 是允 。 为是会在每 为 一次出 时在控制台上显 一条 告消息。到了 Java 16, 时 反射式 也是 强制执 。为了未 地应对 变化 Java 9到16 java启动器 有一个--illegabaccess标志 它有4 可*

- *1. --iUegabaccess=perniit是Java 9默认的行为 它会在每一 法 一次出 时打 印一条消息。*
  - *2. --iUegabaccess=warn对每次 法 打印一条消息。*
  - *3. --iUegabaccess=debug对每次 法 打印一条消息和栈 。*
  - *4. -iUegabaccess=deny是Java 16的默认行为 接拒 所有 法 。*
  - *••illegal-access标志在Java 17巾已 不可 了。*
  - *•-add-exports和-add <sup>叩</sup>ens标志使我们可以 来 整 应 序。*

*样 一个应 序 它使 了一个不再 内 API,例如com.sun. rowset.CachedRowSetlmpl。最好 决方案就是修改 个实 。 在Java 7中 可以从RowSet-Provider中 取一个 冲 。 但是 假 我们不 源代 。*

*在 情况下 -add-exports标志启动 应用程序 指定希望导出 模块和包 以及 将包导出到 模块 在我们所举 例子中 包会导出到不具名模块中。*

*java --add-exports java.sql.rowset/com.sun.rowset=ALL\_UNNAMED \ -jar MyApp.jar*

*在 假 我们 应 序使 反射来 有域或方法 么在不具名模块内 反射 是可 但是对Java平台 公有成员 反射式 就再也不可 了。例如 有些动态 成Java 库会 反射来 受保护 ClassLoader.defineClass方法。如果某个应用程序 使 了 样 库 么 添加下 标志*

*•-add-opens java.base/java.lang=ALL-UNNAMED*

*当添加 些命令 来 应 序工作时 你可 最 会 些吓人 命令 吓 倒。为了更好地管理多个选项 可以将它们放到一个或多个 @前 指定 文件中。例如*

*java @optionsl @options2 -jar MyProg.java*

*其中文件optionsl和叩tions2包含java命令的选项。*

*对于 文件 有多条 关 法 则*

- *・ 格、制 和换 将各个 分*
- *双引号将包括 格在内 参数括 来 例如"Program Files1\**
- *在一 末尾 一个\来合并下一*

- *反斜杠必 义 例如C:\\Users\\Fred*
- *注 以 开头*

### *9.11<sup>传</sup> 求和 <sup>态</sup> <sup>求</sup>*

*在9.4 中 你已 到了 requires 句 基本形式。在本 中 你将 到偶尔会 到 它 两 变体。*

*在某些情况下 对于 定模块 户 声明所有需要的模块会显得很冗 。例如, 一下 java.desktop模块。它需要三个模块 java.prefs、java.datatransfer 和 java.xml,其中 java.prefs模块是在其内 使 。但是 在java.datatransfer和java.xml中的类将出 在公有 API中 就像出 在下 方法中*

```
java• awt• datatransfer.Clipboard java.awt.Toolkit.getSystemClipboard()
java.beans.XMLDecoder(org.xml.sax.InputSource is)
```

*不应 是java.desktop模块 户不得不 。因为 个原因 java.deskt叩模块 transitive修 声明了 求。*

```
module java.desktop
{
   requires java.prefs;
   requires transitive java.datatransfer;
   requires transitive java.xml;
```

*任何声明需要java.desktop 模块 在 动地 两个模块。*

*Q <sup>注</sup> 有些 序员推 在来 另一个模块 包会在公有API<sup>中</sup> 到时 <sup>应</sup> 总是使 requires transitive0但是 并不是Java语言的规则。例如 考虑java.sql模块*

```
module java.sql
{
   requires transitive java.logging;
}
```

*在整个java.sql API中 唯一 到java.logging模块中 包 地方 就是java.sql. Driver.parentLogger 方法 它会 回一个 java.util.logging.Logge「对 。此时 最可接受 方式是不 将 个模块 求声明成传 性 。然后 些 正使 个方法 模块 并且也只有 些模块 声明它们 java.logging<sup>o</sup>*

*requires transitive 句 一 很有吸引力 法是 模块 即没有任何包 只有传 性 求 模块。java.se模块就是 样 模块 它 声明成下 样子*

```
module java.se
   requires transitive java.compiler;
   requires transitive java.datatransfer;
```

```
requires transitive java.desktop;
   requires transitive java.sql;
   requires transitive java.sql.rowset;
   requires transitive java.xml;
   requires transitive java.xml.crypto;
}
```

*对 度模块依 不感兴 序员可以 接声明 java.se,然后 取Java SE平台 所有模块。*

*最 有一 不常 requires static变体 它声明一个模块必 在 时出 在 时是可 。下 是两个 例*

- *1. 在 时 处 注 而该注 是在不同 模块中声明 。*
- *2. 对于位于不同模块中 如果它可 就使 它 否则就执 其他操作 例如*

```
try
   new oracle.jdbc.driver.0racleDriver();
   • • •
}
catch (NoClassDefFoundError er)
{
   Do something else
}
```

### *9.12 定导出和幵放*

*在本 中 你将会 到exports和opens 句 一 变体 将它们 作 域 化到指定 模块 。例如 javafx.base模块包含下 句*

```
exports sun.net to
  java.net.http,
  jdk.naming.dns;
```

*样 句 为 定导出 所列 模块可以 个包 但是其他模块不 。*

*多地使 定导出 明模块化 构比 。尽 如此 在模块化 有代 基时 情况 是会发 。 sun.net包 于java.base模块中 因为 模块最 使 个 包。但是 有几个其他 模块也会 到 个包。Java平台 们并不希望 java.base包 变得更大 并且不希望内 sun.net包变成对所有代 普 可 。在新创建的项冃中 人 们可以设计更模块化 APIo*

*似地 可以将opens 句 制到具体 模块。例如 在9.7 中 我们使 了下 样 的限定opens 句*

```
module v2ch69.openpkg
{
   requires com.horstmann.util;
   opens com.horstmann.places to con.horstmann.util;
}
```

*在 com.horstmann.places 包就只对 com.horstmann.util 模块开放了。*

### *9.13服务加*

*ServiceLoader (卷I <sup>6</sup> )提供了一 机制 于将服务接口与实 <sup>匹</sup> 来。Java平台模块系统使得这种机制更易于使 。*

*下 是对服务加载的一个快 回 。服务拥有一个接口和一个或多个可 实 。下 是一个 单 接口 例*

```
public interface GreeterService
{
  String greet(String subject);
  Locale getLocalef);
}
有一个或多个模块提供了实 例如
public class FrenchGreeter implements GreeterService
{
   public String greet(String subject) { return "Bonjour ・ + subject; }
   public Locale getLocale() { return Locale.FRENCH; }
}
服务消 必 基于其 为 合 标准在提供 所有实 中 择一个。
ServiceLoader<GreeterService> greeterLoader = ServiceLoader.load(GreeterService.class);
GreeterService chosenGreeter;
for (GreeterService greeter : greeterLoader)
{
   if (...)
   {
      chosenGreeter = greeter;
   }
}
```

*在 去 实 是 将文本文件放 到包含实 JAR文件 META-INF/services 录 中 提供 服务消 。模块 提供了一 更好 方式 与提供文本文件不同 可以添 加 句到模块描 中。*

*提供服务实现的模块可以添加一条provides 句 它列出了服务接口(可 定义在任何模 块中) 以及实 (必 是 模块 一 分)。下 是来 jdk.security.auth模块 一个例子*

```
module jdk.security.auth
{
     參
   provides javax.security.auth.spi.LoginModule with
      com.sun.security.auth.module.Krb5LoginModule,
      com.sun.security•auth•module•UnixLoginModule,
      com.sun.security•auth.moduleJndiLoginModule,
      com.sun.security.auth.nodule•KeyStoreLoginModule,
      com.sun.security.auth.module•LdapLoginModule,
      com.sun.security.auth.module.NTLoginModule;
}
```

*与META-INF/services文件 价。*

*使 它 消 模块包含一条uses 句:*

```
module java.base
   uses javax.security•auth.spi.LoginModule;
}
```

*当消 模块中 代 ServiceLoader.load(SerWce/咖</ace.class}时 匹 提供 将 加 尽 它们可 不在可访问的包中。*

*在我们 代 例中 我们为com.horstmann.greetsvc.internal包中 德 和法 候 提 供了 关 实 。 服务模块导出了 com.horstniann.greetsvc包 但是没有导出包含实 包。 provides 句声明了在未导出包中 服务及其实*

```
module com.horstmann.greetsvc
{
   exports com.horstmann.greetsvc;
   provides com.horstmann.greetsvc.GreeterService with
      com.horstmann•greetsvc•internal.FrenchGreeter,
      com.horstmann.greetsvc.internal.GermanGreeterFactory;
}
```

*v2ch69.useservice模块会消 服务。 使 ServiceLoader工具 我们会 代提供 所 有服务 并挑 出匹 所期望 服务*

```
package com.horstmann.hello;
import java.util.*;
import com.horstmann.greetsvc.*;
public class HelloWorld
{
  public static void mdin(String[】args)
  {
     ServiceLoader<Greete「Service〉 greeterLoader
           =ServiceLoader.load(GreeterService.class);
     St ring desiredLanguage = args.length > 9 ? args[6] : "de";
     GreeterService chosenGreeter = null;
     for (GreeterService greeter : greeterLoader)
     {
        if (greeter.getLocaleO.getLanguagef).equals(desiredLanguage))
           chosenCreeter = greeter;
     }
     if (chosenGreeter = null)
        System.out.println("No suitable greeter.");
     else
        System.out.println{chosenGreeter.greet("Modular World1*));
   }
}
  模块声明 服务模块 并声明GreeterService正在 使 。
module v2ch09.useservice
```

7

```
requires com.horstmann.greetsvc;
uses com.horstmann.greetsvc.GreeterService;
```

provides 和 uses 声明的效果,是使消费该服务的模块允许访问私有实现类。 为了构建并运行该程序,首先要编译服务:

```
javac com.horstmann.greetsvc/module-info.java \
   com.horstmann.greetsvc/com/horstmann/greetsvc/GreeterService.java \
   com.horstmann.greetsvc/com/horstmann/greetsvc/internal/*.java
```

#### 然后, 编译并运行消费模块:

```
javac -p com.horstmann.greetsvc \
   v2ch09.useservice/com/horstmann/hello/HelloWorld.java \
   v2ch09.useservice/module-info.java
java -p com.horstmann.greetsvc:v2ch09.useservice \
   -m v2ch09.useservice/com.horstmann.hello.HelloWorld
```

#### 9.14 操作模块的工具

jdeps 工具可以分析给定的 JAR 文件集之间的依赖关系。例如,假设我们想要模块化 Junit 4。运行

jdeps -s junit-4.12.jar hamcrest-core-1.3.jar

-s 标志会产生总结性的输出:

```
hamcrest-core-1.3.jar -> java.base
junit-4.12.jar -> hamcrest-core-1.3.jar
junit-4.12.jar -> java.base
junit-4.12.jar -> java.management
```

它告知了我们下面的模块图:

![](_page_207_Picture_13.jpeg)

如果删除-s标志,那么我们得到的是模块的总结,后面跟着一个映射表,将包映射到所需要的包和模块上。如果添加-v标志,那么列出的清单会将类映射到所需要的包和模块上。

--generate-module-info 选项会对每个分析过的模块产生 module-info 文件:

jdeps --generate-module-info /tmp/junit junit-4.12.jar hamcrest-core-1.3.jar

*0 <sup>注</sup> 有一个 可以 "dot"语言生成 于描 <sup>图</sup> 图形化 <sup>出</sup>。<sup>假</sup> 我们已 安 了 dot工具 么 下 命令*

*jdeps -s -dotoutput /tmp/junit junit-4.12.jar hamcrest-core-1.3.jar dot -Tpng /trip/junit/sumary. dot <sup>&</sup>gt; /tmp/junit/sunnary. png*

*就会得到下 summary.png图*

![](_page_208_Figure_5.jpeg)

*使 jlink工具可以产 执 时无 单 Java 时 境 应 序。所产 像 比整个JDK 小很多。我们可以指定想 包含 模块和 出 录*

*jlink -module-path com. ho rstmann. <sup>g</sup> reet. j <sup>a</sup> r: v2ch09. expo rtedpkg .jar: \$JAVAHOME/j mods \ --add-modules v2ch09.exportedpkg -output /tmp/heUo*

*出 录有一个包含java可执 文件 子 录bin。如果*

*bin/java -m v2ch09.exportedpkg*

*么 模块 主 main方法就会 。*

*jlink 关 是它将 应 序所 最小 模块 打包在一 。我们可以列出其中包 含 所有模块*

*bin/java --list-modules*

*在 个 例中 出是*

*v2ch69.exportedpkg com.horstmann.greet java.base@9*

*所有模块 包含在 时 像文件lib/modules中。在我的计算机上 个文件有23MB, 所有JDK模块 时 像会占据121MBO整个应 占据45MB,只是JDK 一个 头。*

*可以成为 于打包应 序 实 工具 基 。我们仍旧 产 对多平台 文件 和 对应 序 本。*

*1 注 我们可以 j image命令来审 时 像。但是 其格式对JVM来 是内 并且 时 像并不是为其他工具 成并供其他工具所使 。*

*最后 jmod工具可以构建并审 包含在JDK中 模块文件。当査 JDK内 jmods 录 时 会发 对每个模块 有一个扩展名为jniod 文件。 注意 是 在再也没有rt.jar 文件了。*

*与JAR文件一样 些文件也包括 文件。此外 它们 可以包括本地代 库、命令、 头文件、 文件和合法 。JMOD文件使 ZIP文件格式 可以 任意ZIP工具查 它们 内容。*

*与JAR文件不同 JMOD文件只有在 接时才有 也就是 只有在产 时 像 时才有 。我们无 产 JMOD文件 想 将我们 模块与像本地代 库 样 二 制 文件 定。*

*在到了 束Java平台模块 一 时候了。下一 将 另一个 主 : 安全。安全已 成为Java平台 核心 性之一。我们 活和计算的世 正在变得 来 危 彻底理解Java 安全对 多开发 来 性与日俱增。*

## *10 安 <sup>全</sup>*

*▲ <sup>加</sup> <sup>器</sup> ▲数字 <sup>名</sup>*

*▲ 户 ▲加密*

*当Java技术刚刚 世时 令人激动 并不是因为它是一 完 是 因为它 够安全地 因 传播 各 applet。很显然 只有当 户 信applet 代 不会 坏他的计算机时 户才会接受在 上传播 可执 applet。因此 安全是Java 技术 人员和使 所关心 一个 大 。 就意味 Java与其他 和 有 所不同 在 些 和 中安全是在事后才想到 去实 或 是对 坏 一 应对措 施 对java来 安全机制是一个不可分割 成 分。*

*Java安全架构包含下 三个 分*

- *性 对数组的边界进行检査 无不受检査的类型 换 无指 法 。*
- *控制机制 于控制代 够执 操作 比如文件 网络访问等 。*
- *代 名 利用该特性 代 作 就 够 标准 加密 法来 Java代 。 样 代 使 就 够准 地 创建了 代 以及代 名后是否 修 改 。*

*在本书之前 本中 安全 器和代 名 是本 点 但是很显然 在再 它们已 没有意义了。 先 我们来 加 器 它可以在将 加 到 拟机中 时候检查类的完整性。我们将展 机制是如何探测 文件中 损坏 。然后 你 将学习有关 框架和加密 法 内容 它们对于 多安全 关 操作 是 常有*

*一 分已 得了巨大 成功。C++ 序 常很容易 受 如 冲区滥 攻击 但 是Java提供了更强 保护。 憾 是 其他两个 分并不 么成功。安全 器很复杂 且 受攻击 很广。它在Java 17中已 废弃了。代 名架构也 applet和Java web start 两种用于安全地传 客户 应用程序 机制 消亡而遭弃 了。*

### *10.1 <sup>加</sup> <sup>器</sup>*

*Java 器会将源指令 换为 拟机上 代 。 拟机代 存储在以.class为扩展名 文件中 每个 文件 包含某个 或 接口 定义和实 代 。在以下各 中 你将会 到 拟机是如何加 些 文件 。*

#### 10.1.1 类加载过程

请注意,虚拟机只加载程序执行时所需要的类文件。例如,假设程序从 MyProgram.class 开始运行,下面是虚拟机执行的步骤:

- 1. 虚拟机有一个用于加载类文件的机制,例如,从磁盘上读取文件或者请求 Web 上的文件,它使用该机制来加载 MyProgram 类文件中的内容。
- 2. 如果 MyProgram 类拥有类型为另一个类的域,或者拥有超类,那么这些类文件也会被加载。(加载某个类所依赖的所有类的过程称为类的解析。)
  - 3. 接着,虚拟机执行 MyProgram 中的 main 方法(它是静态的,无须创建类的实例)。
  - 4. 如果 main 方法或者 main 调用的方法要用到更多的类,那么接下来就会加载这些类。然而,类加载机制并非只使用单个的类加载器。每个 Java 程序至少拥有三个类加载器:
  - 引导类加载器
  - 平台类加载器
  - 系统类加载器(有时也称为应用类加载器)

引导类加载器负责加载包含在下列模块以及大量的 JDK 内部模块中的平台类:

iava.base

java.datatransfer

java.desktop

java.instrument

java.logging

java.management

java.management.rmi

java.naming

java.prefs

java.rmi

java.security.sasl

java.xml

引导类加载器没有对应的 ClassLoader 对象,例如,方法

StringBuilder.class.getClassLoader()

#### 将返回 null。

在 Java 9 之前, Java 平台类位于 rt.jar 中。如今, Java 平台是模块化的,每个平台模块都包含一个 JMOD 文件(参见第 9 章)。平台类加载器会加载引导类加载器没有加载的 Java 平台中的所有类。

系统类加载器会从模块路径和类路径中加载应用类。

這程:在 Java 9 之前,"扩展类加载器"会加载 jre/lib/ext 目录中的"标准扩展",而"授权标准覆盖"机制提供了一种方式,可以用更新的版本覆盖某些平台类(包括 CORBA 和 XML 的实现)。这两种机制都被移除了。

#### 10.1.2 类加载器的层次结构

类加载器有一种父/子关系。除了引导类加载器外,每个类加载器都有一个父类加载器。

*根据 定 加 器会为它 加 器提供一个机会 去加 任何 定 并且只有在其 加 器加 失 时 它 才会加 定 。例如 当 求 加 器加 一个 (比如 java.lang.StringBuiUfer)时 它 先 求平台 加 器 加 加 器则 先 求引导 加 器 加 。引导 加 器会找到并加 个 无 其他 两个 加 器做 更多 搜 。*

*某些 序具有插件架构 其中代 某些 分是作为可 插件打包 。如果插件 打 包为JAR文件 就可以 接 URLClassLoader 实例去加 插件 。*

```
var url = new URL(Bfile:///path/to/plugin.jarB);
var pluginLoader = new URLClassLoader(new URL[] { url });
Class<?> cl = pluginLoader.loadClass("rnypackage.MyClass");
```

*于在URLClassLoader构 器中没有指定 加 器 因此pluginLoader的父类加 器就是 加 器。图10-1展 了 层次 构。*

![](_page_212_Figure_5.jpeg)

*图10-1 <sup>加</sup> <sup>器</sup> 层次 <sup>构</sup>*

*令 吿 在Java9之前 加 器是URLClassLoaser 实例。有些 序员会使 强 制 型来 其getURLs方法 或 反射机制 受保护 addURLs方法将JAR文 件添加到 径中。 在无法 样操作了。*

*大多数时候 你不必操心 加 器 层次 构。 常 是 于其他 它 加*

*个 对你是 明 。*

*偶尔 你也会 干涉和指定 加 器。 下 例子*

- *你 应 代 包含一个助手方法 它要调用Class.forName(classNameString)<sup>o</sup>*
- *・ 个方法是从一个插件 中 。*
- *• classNameString指定 正是一个包含在 个插件 JAR中的类。*

*插件 作 期望 个 会 加 。但是 助手方法 是 加 器加 正 是Class.forName所使 加 器。 对于它来 插件JAR中 是不可 为 加我器倒 。*

*决 个 助手方法 使 恰当 加 器 它可以 求 加 器作为它 一 个参数传递给它。或 它可以 求将恰当 加 器 成为当前 上下文 加 器 在 多框架中 得到了应 (例如JAXP和JNDI)。*

*每个 有一个对 加 器 引 为上下文 加 器。主 上下文 加 器 是 加 器。当新 创建时 它 上下文 加 器会 成为创建 上下文 加 器。因此 如果不做任何 殊 操作 么所有 就 会将它们 上下文 加 器 为 加 器。*

*但是 我们也可以 下 将其 成为任何 加 器。*

*Thread t <sup>=</sup> Thread.currentThread(); t.setContextClassLoader(loader);*

*然后助手方法可以 取 个上下文 加 器*

*Thread t <sup>=</sup> Th read.cu rrentThread(); ClassLoader loader = t.getContextClassLoaderf); Class<?> cl <sup>=</sup> loader.loadClass(className);*

*0 <sup>提</sup> 如果你 写了一个按名字来加 方法 么让调用者在传 显式的类加 器和使 上下文 加 器之 择是一 好 做法。不 接使 方法所属 加 器。*

#### *10.1.3将 加 器 作命名*

*每个Java 序员 包 命名是为了消 名字冲 。在标准 库中 有两个名为 Date 它们 实 名字分别为java.util.Date和java.sql.Date。使 单 名字只是为了 方便 序员 它们 求 序包含恰当 import 句。在一个正在执 序中 所有的类名 包含它们 包名。*

*然 令人惊奇 是 在同一个 拟机中 可以有两个 它们 名和包名 是 同 。 是 它 全名和 加 器来 定 。 技术在加 来 多处 代 时很有 。例 如 应 服务器会为每一个应 使 单 加 器 使 拟机可以区分来 不同应 无 它们是怎样命名 。图10-2展 了一个 例。假 一个应 服务器加 了两个不* 同的应用,它们都有一个名为 Util 的类。因为每个类都是由单独的类加载器加载的,所以这些类可以彻底地区分开而不会产生任何冲突。

#### 10.1.4 编写你自己的类加载器

我们可以编写自己的用于特殊目的的类加载器, 这使我们可以在向虚拟机传递字节码之前执行定制的 检查。例如,我们可以编写一个类加载器,它可以拒 绝加载没有标记为"paid for"的类。

如果要编写自己的类加载器,只需要继承 ClassLoader类,然后覆盖下面这个方法:

findClass(String className)

ClassLoader 超类的 loadClass 方法用于将类的加载操作委托给其父类加载器去进行,只有当该类尚未加载并且父类加载器也无法加载该类时,才调用findClass 方法。

如果要实现该方法,必须做到以下几点:

- 1. 为来自本地文件系统或者其他来源的类加载其字节码。
- 2. 调用 ClassLoader 超类的 defineClass 方法,向虚拟机提供字节码。

在程序清单 10-1 中, 我们实现了一个类加载器, 用于加载加密过的类文件。该程序要求用户输入第 一个要加载的类的名字(即包含 main 方法的类)和密 钥。然后,使用一个专门的类加载器来加载指定的类

![](_page_214_Figure_11.jpeg)

图 10-2 两个类加载器分别加载具有 相同名字的两个类

并调用 main 方法。该类加载器对指定的类和所有被其引用的非系统类进行解密。最后,该程序会调用加载好的类的 main 方法 (参见图 10-3)。

为了简单起见,我们忽略了密码学领域 2000 年来所取得的技术进展,而是采用了传统的 Caesar 密码对类文件进行加密。

**注释:** David Kahn 的佳作 *The Codebreakers* (纽约 Macmillan 出版社 1967 年出版) 第84页中称 Suetonius 是 Caesar 密码的发明人。Caesar 将罗马字母表的 24 个字母移动了 3 个字母的位置,在那个时代这可以迷惑对手。

第一次撰写本章时,美国政府限制高强度加密方法的出口。因此,我们在实例中使用的是 Caesar 的加密方法,因为该方法的出口显然是合法的。

我们的 Caesar 密码版本使用的密钥是 1~255 之间的一个数字,解密时,只需将密钥与每个字节相加,然后对 256 取余。程序清单 10-2 的 Caesar. java 程序就实现了这种加密行为。

![](_page_215_Figure_2.jpeg)

图 10-3 ClassLoaderTest 程序

为了不与常规的类加载器相混淆,我们对加密的类文件使用了不同的扩展名.caesar。

解密时,类加载器只需要将每个字节减去该密钥即可。在本书的程序代码中,可以找到4个类文件,它们都是用"3"这个传统的密钥值进行加密的。为了运行加密程序,需要使用在我们的 ClassLoaderTest 程序中定义的定制类加载器。

对类文件进行加密有很多用途(当然,使用的密码的强度应该高于 Caesar 密码的),如果没有加密密钥,类文件就毫无用处。它们既不能由标准虚拟机来执行,也不能轻易地被反汇编。

这就是说,可以使用定制的类加载器来认证类用户的身份,或者确保程序在运行之前已 经支付了软件费用。当然,加密只是定制类加载器的应用之一。可以使用其他类型的加载器 来解决别的问题,例如,将类文件存储到数据库中。

#### 程序清单 10-1 classLoader/ClassLoaderTest.java

```
package classLoader;
3 import java.io.*;
4 import java.lang.reflect.*;
5 import java.nio.file.*;
6 import java.awt.*;
7 import java.awt.event.*;
8 import javax.swing.*;
9
10 /**
* This program demonstrates a custom class loader that decrypts class files.
   * @version 1.25 2018-05-01
12
   * @author Cay Horstmann
13
15 public class ClassLoaderTest
16 {
      public static void main(String[] args)
17
18
         EventQueue.invokeLater(() ->
19
28
```

```
var frame = new ClassLoaderFrame();
21
               frame.setTitle("ClassLoaderTest");
22
               frame.setDefaultCloseOperation(JFrame.EXIT ON CLOSE);
23
                frame.setVisible(true);
24
            });
25
26
27
28
29
    * This frame contains two text fields for the name of the class to load and the
38
    * decryption key.
31
32
   class ClassLoaderFrame extends JFrame
33
34
      private JTextField keyField = new JTextField("3", 4);
35
      private JTextField nameField = new JTextField("Calculator", 30);
36
      private static final int DEFAULT WIDTH = 300;
37
      private static final int DEFAULT HEIGHT = 200;
38
30
       public ClassLoaderFrame()
48
       {
41
42
          setSize(DEFAULT WIDTH, DEFAULT HEIGHT);
          setLayout(new GridBagLayout());
43
          add(new JLabel("Class"), new GBC(0, 0).setAnchor(GBC.EAST));
44
          add(nameField, new GBC(1, 0).setWeight(100, 0).setAnchor(GBC.WEST));
45
46
          add(new JLabel("Key"), new GBC(0, 1).setAnchor(GBC.EAST));
          add(keyField, new GBC(1, 1).setWeight(100, 0).setAnchor(GBC.WEST));
47
48
          var loadButton = new JButton("Load");
          add(loadButton, new GBC(0, 2, 2, 1));
49
          loadButton.addActionListener(
50
             event -> runClass(nameField.getText(), keyField.getText()));
51
52
          pack();
53
54
55
        * Runs the main method of a given class.
56
        * @param name the class name
57
        * @param key the decryption key for the class files
58
59
       public void runClass(String name, String key)
60
       {
61
          try
62
63
             var loader = new CryptoClassLoader(Integer.parseInt(key));
64
             Class<?> c = loader.loadClass(name);
             Method m = c.getMethod("main", String[].class);
66
             m.invoke(null, (Object) new String[] {});
67
          }
68
          catch (Throwable t)
69
78
             JOptionPane.showMessageDialog(this, t);
71
72
73
   }
74
75
```

```
/**
76
    * This class loader loads encrypted class files.
   class CryptoClassLoader extends ClassLoader
79
80
      private int key;
81
82
83
       * Constructs a crypto class loader.
84
       * @param k the decryption key
85
86
      public CryptoClassLoader(int k)
87
88
         key = k;
89
98
91
      protected Class<?> findClass(String name) throws ClassNotFoundException
92
93
94
         try
95
             byte[] classBytes = null;
96
             classBytes = loadClassBytes(name);
97
             Class<?> cl = defineClass(name, classBytes, 0, classBytes.length);
98
             if (cl == null) throw new ClassNotFoundException(name);
             return cl;
100
101
          catch (IOException e)
193
             throw new ClassNotFoundException(name);
194
196
107
198
        * Loads and decrypt the class file bytes.
189
        * @param name the class name
110
        * @return an array with the class file bytes
111
112
       private byte[] loadClassBytes(String name) throws IOException
113
114
          String cname = name.replace('.', '/') + ".caesar";
115
          byte[] bytes = Files.readAllBytes(Path.of(cname));
          for (int i = 0; i < bytes.length; i++)
117
             bytes[i] = (byte) (bytes[i] - key);
118
          return bytes;
120
121 }
```

#### 程序清单 10-2 classLoader/Caesar.java

```
package classLoader;
\nimport java.io.*;

/**
```

```
6
9
18
11
12
U
14
15
16
17
18
19
26
21
22
23
27
28
29
昶
31
32
    * Encrypts a file using the Caesar cipher.
    * ^version 1.62 2618-05-01
    * @author Cay Horstmann
    */
   public class Caesar
   {
      public static void main(String[] args) throws Exception
      {
          if (args.length !« 3)
          {
             System.out.printin("USAGE: java classLoader.Caesar in out key");
             return;
          }
          try (var in = new FileInputStream(args[0]);
                 var out • new FileOutputStreatn(args[ 1]))
          {
             int key = Integer.parseInt(args【2D;
             int ch;
             while ((ch = in.readO) != -1)
             {
                 byte c = (byte) (ch + key);
                 out.write(c)
             }
          }
       }
   }
```

#### *叫 java.lang.Class*

*• ClassLoader getClassLoader() 取加 加 器。*

#### *aiava.lang.ClassLoader*

- *• ClassLoader getParent() 1.2 回 加 器 如果 加 器是引导 加 器 则 回nuU。*
- *• static ClassLoader getSystemClassLoaderO 1.2 取 加 器 即 于加 一个应 加 器。*
- *• protected Class findClass(String name) <sup>2</sup> 加 器应 方法 以查找类的字节码 并通过调用defineClass方法将字 传给虚拟机。在类的名字中 使 .作为包名分隔符 并且不使 .class后 。*
- *• Class defineClass(String name, byte[] byteCodeData, int offset, int length) 将一个新 添加到 拟机中 其字 在 定 数据 围中。*

#### *java.net.URLCUssLoader*

- *• URLClassLoader(URL[] urls)*
- *• URLClassLoader(URL[l urls, ClassLoader parent)*

*构建一个 加 器 它可以从 定 URL处加 。如果URL以/ 尾 么它 是一个 录 否则 它 是一个JAR文件。*

#### *叫 java.lang.Thread*

- *<sup>參</sup> ClassLoader getContextClassLoader 取 加 器 创建 将其指定为执 时最 合使 加 器。*
- *• void setContextClassLoader ClassLoader loader 为 中 代 一个 加 器 以 取 加 。如果在启动一个 时没 有显式地 上下文 加 器 则使用父线程的上下文 加 器。*

#### *10.1.5 字节码校*

*当 加 器将新加载的Java平台 字 传 拟机时 些字 昏先 接受校 器 verifier 校 。校 器 检査 些指令无法执 明显有 坏性 操作。 了 外 所有 校 。*

*下 是校 器执 一些检査*

- *变 在使 之前 初始化。*
- *方法 与对 引 型之 匹 。*
- *有数据和方法 则没有 反。*
- *对本地变 在 时栈内。*
- *时栈没有溢出。*

*如果以上 些检査中任何一条没有 么 就 为 到了 坏 并且不予 加 。*

*注 如果 悉Godel定 么你可 想 校 器 是如何 明某个 文件不 存在 型不匹 、变 没有初始化和栈溢出 。根据Gddel定 不可能设计 出 样 法 它 够处 序 定其是否具有 定 属性 比如不出 栈溢出 。 是否属于Oracle公司 公共关系部门和逻辑法则之间的矛盾呢 不— 事实 上 校 器并 是一个Godel意义上 决 法。如果校 器接受了一个 序 么 序就 实是安全 。然 也有 多 序尽 是安全 但却 校 器拒 了。 在强制 哑元值来初始化一个变 时 你就会 到 个 因为 器无法了 个变 是否可以 正 地初始化。*

*这种严格 校 是出于安全上的考虑 有一些偶然性 比如变 没有初始化 如 果没有 捕 就很容易对 成严 坏。更为 是 在因 样开放 境 中 你必 保护 己以 恶意 序员对你实施攻击 因为他们 就是 成恶劣 影 响。例如 修改 时栈中 值 或 向 对 有实例域写入数据 某个 序就 会 浏 器 安全 。*

*当然 你可 想 为什么 有一个专 校 器来检査 些 性。毕 编译器 不*