import org.jsoup.Connection;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import java.io.IOException;
import java.util.ArrayList;

public class Memes {

    private StringBuilder site = new StringBuilder();
    private ArrayList<String> addresses = new ArrayList<>();

    public String memes(int amount){
        addresses.add("https://kwejk.pl");
        addresses.add("https://besty.pl");
        try{
            for (String url: addresses) {
                //Connect to URL address
                Connection connect = Jsoup.connect(url);
                //Start each block with URL address of the currently browsed www site
                site.append("<h1>").append(url).append("</h1>");
                //Get www site as Document object
                Document document = connect.get();
                //Find all images on site
                //TODO 1.2 znajdź wszystkie obrazki w kodzie strony. Zapisz je do zmiennej allIMG
                Elements allImg = document.select("img");
                //Search through all images found on site
                if (url.equals("https://kwejk.pl")) {
                    //TODO 1.2 przeanalizuj kod, zwracany jako poszczególne elementy, a następnie wyświetl tylko amount
                    //TODO 1.2 pierwszych memów z serwisu kwejk.pl
                    for (Element img : allImg.subList(0, Math.min(amount, allImg.size()))) {
                        //Handle relative addresses
                        if (img.attr("src").startsWith("/")){
                            site.append("<div class = 'container'><img src='").append(url);
                            site.append(img.attr("src")).append("'></div>");
                        } else {
                            site.append("<div class = 'container'><img src='").append(img.attr("src"));
                            site.append("'></div>");
                        }
                    }



                } else if (url.equals("https://besty.pl")) {
                    //TODO 1.2 Serwis besty.pl wyrzuca niepotrzebne nam śmieci jako 2 pierwsze obrazki.
                    //TODO 1.2 Za pomocą metody sublist() odzyskaj amount pierwszych memów
                    for (Element img : allImg.subList(2, Math.min(amount, allImg.size()))) {
                        //Handle relative addresses
                        if (img.attr("src").startsWith("/")){
                            site.append("<div class = 'container'><img src='").append(url);
                            site.append(img.attr("src")).append("'></div>");
                        } else {
                            site.append("<div class = 'container'><img src='").append(img.attr("src"));
                            site.append("'></div>");
                        }
                    }

                } else {
                    for (Element img : allImg.subList(0, Math.min(amount, allImg.size()))) {
                        //Handle relative addresses
                        if (img.attr("src").startsWith("/")){
                            site.append("<div class = 'container'><img src='").append(url);
                            site.append(img.attr("src")).append("'></div>");
                        } else {
                            site.append("<div class = 'container'><img src='").append(img.attr("src"));
                            site.append("'></div>");
                        }
                    }
                }
            }
        } catch (IOException e){
            System.err.println(e);
        }
        return site.toString();
    }
}
