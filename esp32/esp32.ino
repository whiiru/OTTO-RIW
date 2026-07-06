#include <WiFi.h>
#include <WebServer.h>

// Insira suas credenciais de Wi-Fi
const char* ssid = "NOME DA REDE";
const char* password = "SENHA DA REDE";

// Inicia o servidor web na porta HTTP padrão (80)
WebServer server(80);

const int ledPin = 32; 

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); // Garante que comece desligado

  // Conexão Wi-Fi
  Serial.print("Conectando a ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Wi-Fi conectado.");
  Serial.print("Endereço IP do ESP32: ");
  Serial.println(WiFi.localIP()); // ANOTE ESTE IP PARA USAR NO PYTHON

  // Configuração das rotas (Endpoints)
  server.on("/led/on", []() {
    digitalWrite(ledPin, HIGH);
    server.send(200, "text/plain", "LED Ligado com sucesso");
    Serial.println("Comando recebido: LIGAR");
  });

  server.on("/led/off", []() {
    digitalWrite(ledPin, LOW);
    server.send(200, "text/plain", "LED Desligado com sucesso");
    Serial.println("Comando recebido: DESLIGAR");
  });

  server.begin();
  Serial.println("Servidor HTTP iniciado.");
}

void loop() {
  // Mantém o servidor escutando requisições dos clientes
  server.handleClient();
  delay(2); // Pequeno delay para estabilidade
}