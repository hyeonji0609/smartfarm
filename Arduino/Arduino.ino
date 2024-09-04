#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <time.h>
#include "config.h"

#define CAMERA_MODEL_AI_THINKER // Has PSRAM
#include "camera_pins.h"

const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 0;  // GMT 시간 오프셋 (한국은 GMT+9 이므로 32400초)
const int daylightOffset_sec = 0;

void setup() {
  Serial.begin(115200);
  Serial.println();

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
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
  config.frame_size = FRAMESIZE_UXGA;
  config.pixel_format = PIXFORMAT_JPEG;
  config.fb_location = CAMERA_FB_IN_PSRAM;
  config.jpeg_quality = 10;
  config.fb_count = 1;

  if (psramFound()) {
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.fb_location = CAMERA_FB_IN_DRAM;
  }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    camera_fb_t * fb = esp_camera_fb_get(); // 사진 찍는 부분
    if (!fb) {
      Serial.println("Camera capture failed");
      return;
    }

    HTTPClient http; // http 객체 생성
    http.begin(serverName); // http 요청 시작
    http.addHeader("Content-Type", "image/jpeg");
    http.addHeader("device-id", deviceId);  // 고유 ID를 헤더에 추가

    Serial.println(WiFi.localIP()); // ESP32-CAM의 로컬 IP 주소 출력
    Serial.printf("Attempting to connect to server: %s\n", serverName);

    int httpResponseCode = http.POST(fb->buf, fb->len);

    if (httpResponseCode > 0) {
      Serial.printf("Image sent, HTTP response code: %d\n", httpResponseCode);
      Serial.printf("==========================================");
    } else {
      Serial.printf("Error sending image, HTTP response code: %d\n", httpResponseCode);
      Serial.printf("==========================================");
    }

    http.end();
    esp_camera_fb_return(fb);

    delay(10000);  // 10초 대기
  } else {
    Serial.println("WiFi Disconnected");
  }
}
