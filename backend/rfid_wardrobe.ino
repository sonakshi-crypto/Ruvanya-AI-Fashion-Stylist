#include <SPI.h>
#include <MFRC522.h>
#include <WiFi.h>
#include <HTTPClient.h>

#define SS_PIN 5
#define RST_PIN 21

MFRC522 rfid(SS_PIN, RST_PIN);

// Wokwi Wi-Fi
const char* WIFI_SSID = "Wokwi-GUEST";
const char* WIFI_PASSWORD = "";

// FastAPI server
const char* SERVER_URL =
  "http://10.20.73.115:8000/wardrobe/rfid";

void setup() {

  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi connected!");

  // Start RFID
  SPI.begin();
  rfid.PCD_Init();

  Serial.println("Smart Wardrobe RFID Ready");
  Serial.println("Waiting for clothing tag...");
}

void loop() {

  // Check for RFID card
  if (!rfid.PICC_IsNewCardPresent()) {
    return;
  }

  if (!rfid.PICC_ReadCardSerial()) {
    return;
  }

  // Create UID string
  String uid = "";

  Serial.print("RFID UID: ");

  for (byte i = 0; i < rfid.uid.size; i++) {

    if (rfid.uid.uidByte[i] < 0x10) {
      Serial.print("0");
      uid += "0";
    }

    Serial.print(rfid.uid.uidByte[i], HEX);
    uid += String(rfid.uid.uidByte[i], HEX);

    if (i < rfid.uid.size - 1) {
      Serial.print(":");
      uid += ":";
    }
  }

  Serial.println();

  // Convert UID to uppercase
  uid.toUpperCase();

  // Identify clothing
  if (uid == "01:02:03:04") {
    Serial.println("Clothing Item: Black T-Shirt");
  }
  else if (uid == "11:22:33:44") {
    Serial.println("Clothing Item: Blue Jeans");
  }
  else if (uid == "55:66:77:88") {
    Serial.println("Clothing Item: Red Dress");
  }
  else {
    Serial.println("Clothing Item: Unknown");
  }

  // Send UID to FastAPI
  if (WiFi.status() == WL_CONNECTED) {

    HTTPClient http;

    Serial.println("Sending wardrobe data...");

    http.begin(SERVER_URL);
    http.addHeader("Content-Type", "application/json");

    String json = "{\"uid\":\"" + uid + "\"}";

    int responseCode = http.POST(json);

    //Serial.print("Backend response: ");
    //Serial.println(responseCode);

    if (responseCode > 0) {
      String response = http.getString();
      Serial.println("Backend says:");
      Serial.println(response);
    }
    else {
      //Serial.println("Could not connect to backend.");
    }

    http.end();
  }

  Serial.println("-------------------------");

  rfid.PICC_HaltA();

  delay(2000);
}
