import oscP5.*;
import netP5.*;
import processing.sound.*;

StringList textsToDisplay;

OscP5 oscP5;

NetAddressList myNetAddressList = new NetAddressList();

/* listeningPort is the port the server is listening for incoming messages */
int myListeningPort = 5006;
/* the broadcast port is the port the clients should listen for incoming messages from the server*/
int myBroadcastPort = 6969;

String levelPattern = "/level";
String pathraWordsPattern = "/pathraspeak";
String playerWordsPattern = "/playerspeak";

JSONArray transitions;

void setup() {
  size(1200,1200);
  oscP5 = new OscP5(this, myListeningPort);
  frameRate(25);
  textsToDisplay = new StringList();
  transitions = loadJSONArray("data.json");
}


void draw() {
  background(0);
  textSize(26);
  for ( int i = 0; i < textsToDisplay.size(); i++){
     text(textsToDisplay.get(i), width/2, height/8 + i*50);
  }
}

void oscEvent(OscMessage theOscMessage) {
  if (theOscMessage.addrPattern().equals(levelPattern)) {
    //Got next level, play sound and display text
    SoundFile sound = new SoundFile(this, transitions[theOscMessage.arguments[0]].sound);
    String txt = transitions[theOscMessage.arguments[0]].txt;
    textsToDisplay.clear();
    textsToDisplay.append(txt);
    sound.play();

  }
  else if (theOscMessage.addrPattern().equals(pathraWordsPattern)) {
    updateText(theOscMessage.arguments[0]);

  }
  else if (theOscMessage.addrPattern().equals(playerWordsPattern)) {
    textsToDisplay.append(theOscMessage.arguments[0]);

  }
}

private void updateText(String newLine){
  if(textsToDisplay.size()>10) textsToDisplay.clear();
  textsToDisplay.append(newLine);
}


 private void connect(String theIPaddress) {
     if (!myNetAddressList.contains(theIPaddress, myBroadcastPort)) {
       myNetAddressList.add(new NetAddress(theIPaddress, myBroadcastPort));
       println("### adding "+theIPaddress+" to the list.");
     } else {
       println("### "+theIPaddress+" is already connected.");
     }
 }



private void disconnect(String theIPaddress) {
if (myNetAddressList.contains(theIPaddress, myBroadcastPort)) {
    myNetAddressList.remove(theIPaddress, myBroadcastPort);
       println("### removing "+theIPaddress+" from the list.");
     } else {
       println("### "+theIPaddress+" is not connected.");
     }
       println("### currently there are "+myNetAddressList.list().size());
 }
