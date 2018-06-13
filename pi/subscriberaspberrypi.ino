// -----------------------------------------
// Subscribe and Turn Off Crit/NonCrit Relay

int relay1 = TX;
int relay2 = RX;
int relay3 = D0;
int battCharge;

// We start with the setup function.

void setup() {
  // This part is mostly the same:
  pinMode(relay1,OUTPUT); // Our LED pin is output (lighting up the LED)
  pinMode(relay2,OUTPUT); // Our on-board LED is output as well
  pinMode(relay3,OUTPUT); // The pin powering the photoresistor is output (sending out consistent power)

  // Here we are going to subscribe to your buddy's event using Particle.subscribe
  Particle.subscribe("P2P_State_of_Charge", myHandler);
  // Subscribe will listen for the event buddy_unique_event_name and, when it finds it, will run the function myHandler()
  // (Remember to replace buddy_unique_event_name with your buddy's actual unique event name that they have in their firmware.)
  // myHandler() is declared later in this app.
}


void loop() {
  
}


// Now for the myHandler function, which is called when the cloud tells us that our buddy's event is published.
void myHandler(const char *event, const char *data)
{
  battCharge = stoi(data);
  if (battCharge < 50){
      
  }
  
  /* Particle.subscribe handlers are void functions, which means they don't return anything.
  They take two variables-- the name of your event, and any data that goes along with your event.
  In this case, the event will be "buddy_unique_event_name" and the data will be "intact" or "broken"

  Since the input here is a char, we can't do
     data=="intact"
    or
     data=="broken"

  chars just don't play that way. Instead we're going to strcmp(), which compares two chars.
  If they are the same, strcmp will return 0.
  */

  if (strcmp(data,"intact")==0) {
    // if your buddy's beam is intact, then turn your board LED off
    digitalWrite(boardLed,LOW);
  }
  else if (strcmp(data,"broken")==0) {
    // if your buddy's beam is broken, turn your board LED on
    digitalWrite(boardLed,HIGH);
  }
  else {
    // if the data is something else, don't do anything.
    // Really the data shouldn't be anything but those two listed above.
  }
}

