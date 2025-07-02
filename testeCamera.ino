#include "esp_camera.h"
#include <WiFi.h>

#define TEMPO_FOTO 1000 //1 segundo



const char* ssid = "ESP32-CAM-REDE";
const char* password = "ultrabots3";


IPAddress local_IP(192,168,4,1);
IPAddress gateway(192,168,4,1);
IPAddress subnet(255,255,255,0);


IPAddress raspberry_ip(192,168,4,2);
const uint16_t raspberry_port  = 5000;

WiFiServer dummyServer(80); // Só pra manter o AP ativo

#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22



void setup(){

  Serial.begin(115200);
  delay(1000);

  WiFi.softAPConfig(local_IP, gateway, subnet);
  WiFi.softAP(ssid, password);

  dummyServer.begin(); // Mantém o AP estável

  Serial.println("Rede Wi-Fi criada!");
 // Serial.print("SSID: ");
  //Serial.println(ssid);
  //Serial.print("Senha: ");
  //Serial.println(password);
  //Serial.print("IP do ESP32: ");
  Serial.println(WiFi.softAPIP());

  camera_config_t config;

  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;                      //INICIALIZA A CAMERA
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.fb_location = CAMERA_FB_IN_DRAM;

  if(psramFound()){
    config.frame_size = FRAMESIZE_VGA;       //CONFERE SE O ESP TEM RAM EXTERNA  
    config.jpeg_quality = 10;                //SO PARA TESTE TIRAR DEPOIS
    config.fb_count = 2;
  }else{
      config.fb_location = CAMERA_FB_IN_DRAM;
      config.frame_size = FRAMESIZE_CIF;
      config.jpeg_quality = 12;
      config.fb_count = 1;
  }


  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Erro ao iniciar a câmera");         //VAI FALHAR NO SIMULADOR
    while (true);                                       //TRAVA O PROGRAMA CASO A CAMERA NAO FUNCIONE
                                                        //EXISTEM OUTRAS OPÇOES COMO REINICIAR AUTOMATICAMENTE
  }

  Serial.println("Câmera pronta. Iniciando fotos...");
}

int fotoAtual = 0;
unsigned long ultimaFoto = 0;
WiFiClient client;


void loop(){

  if(fotoAtual < 300 && millis() - ultimaFoto >= TEMPO_FOTO){

    
    if(!client.connected()){
      if (!client.connect(raspberry_ip, raspberry_port)) {
        Serial.println("Erro ao conectar com Raspberry");
        return;
      }
    
    } 
    
    Serial.printf("Capturando foto %d...\n",fotoAtual+1);
    camera_fb_t *fb = esp_camera_fb_get();

    if(!fb){
      Serial.println("Erro ao capturar foto!");
      return;
    }

      uint32_t img_size = fb->len; 
      client.write((uint8_t*)&img_size, sizeof(img_size));
      client.write(fb->buf, fb->len);

    fotoAtual++;
    esp_camera_fb_return(fb);
    ultimaFoto = millis();
  }
}
