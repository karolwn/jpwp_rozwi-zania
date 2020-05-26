import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

import javax.swing.*;
import java.io.*;
import java.net.InetAddress;
import java.net.Socket;

public class Client {

    private static final int port = 1488;
    private static InetAddress host;

    private static Socket socket;

    public void show(Document site, String title){
        JEditorPane jep = new JEditorPane("text/html", site.toString());
        jep.setEditable(false);
        jep.addHyperlinkListener(new LinkFollower());
        JScrollPane pane = new JScrollPane(jep);
        JFrame f = new JFrame(title);
        f.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        f.setContentPane(pane);
        f.setSize(800, 600);
        f.show();
    }

    public void connection(String type, String title, String args) {
        try {
            //Getting localhost ip
            host = InetAddress.getByName("localhost");

            //Establish connection with Server
            //TODO 2.3 Utwórz socket z adresem host na porcie port
            socket = new Socket(host, port);

            //Obtaining input and output streams
            //TODO 2.3 Utórz przychodzący i wychodzący strumień danych, zapisz je jako in oraz out

            DataInputStream in = new DataInputStream(new InputStream() {
                @Override
                public int read() throws IOException {
                    return 0;
                }
            });
            DataOutputStream out = new DataOutputStream(new OutputStream() {
                @Override
                public void write(int b) throws IOException {

                }
            });


            //Sending data to ClientHandler
            out.writeUTF(type);
            out.writeUTF(args);
            if (!type.equals("subscription")) {
                String input = in.readUTF();
                //TODO 2.3 Wykonaj parsowanie strony internetowej i wyświetl ją za pomocą funkcji show(...)
                

            }
            out.close();
            in.close();
            socket.close();
        } catch (Exception e){
            System.err.println("Error 503: Service Unavailable");
        }
    }
}
