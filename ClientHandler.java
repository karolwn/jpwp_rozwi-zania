import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

class ClientHandler {

    public ClientHandler(Server server, Socket socket, DataInputStream in, DataOutputStream out){

        String input;
        String output;

        try {
            //Read data from client
            //TODO 2.2 Zdobądź dane od klienta i zapisz je do zmiennej input
            input = in.readUTF();

            switch (input) {
                //Handle client requests
                //TODO 2.2 Obsłuż żądania klienta. Dla ułatwienia pozostawiono tyle pustych linii, ile powinien zajmować kod
                case "infos":




                    break;
                case "memes":




                    break;
                case "subscription":
                    String newSubscriber = in.readUTF();
                    //Variable for checking existence of client on subscriber list
                    Boolean newAddress = true;
                    //Check is client appears on subscriber list
                    for (String subscriber: server.getCoronavirusSubscribers()){
                        if (newSubscriber.equals(subscriber)){
                            newAddress = false;
                        }
                    }
                    //If it is truly a new client add him to subscriber list
                    if (newAddress) {
                        server.addSubscriber(newSubscriber);
                    }
                    break;
                default:
                    System.err.println("Something went wrong!");
                }
                socket.close();
                in.close();
                out.close();
        } catch (IOException e){
            System.err.println(e);
        }
    }
}
