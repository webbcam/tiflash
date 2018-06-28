importPackage(java.io);
importPackage(java.net);
//importPackage(Packages.org.mozilla.javascript);

SERVER = "localhost"
PORT = 19876

function post_result(port, result)
{
    var connection = new Socket(SERVER, port);
    var connection_out = new PrintWriter(connection.getOutputStream(), true);
    //var connection_in = new BufferedReader(new InputStreamReader(connection.getInputStream()));

//    var context = Context.enter();
//    var scope = context.initStandardObjects();
//    var json = NativeJSON.stringify(context, scope, result, null, null);

    //  Send result then close socket
    connection_out.println(result);
    connection_out.close();
    connection.close();

    return true;
}
