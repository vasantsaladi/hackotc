import haxe.Http;
import js.Browser;
import js.html.Element;

class Sample {
    static public function main() {
        // Find the container which will hold the results
        var container:Element = Browser.document.getElementsByTagName('pre')[0];

        // Create a new HTTP request
        var http:Http = new Http('./test');
        
        // Handle the response
        http.onData = function(response:String) {
            // Set the container's text to our response
            container.innerText = response;
        };
        
        // Handle errors
        http.onError = function(error:String) {
            // If an error comes up, report it!
            Browser.console.error(error);
        };

        // Send the request
        http.request(false); // false indicates a GET request; true would indicate a POST request
    }
}
