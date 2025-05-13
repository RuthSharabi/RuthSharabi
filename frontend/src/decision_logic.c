#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "cJSON.h"

// פונקציה המחשבת את הפעולה הבאה
const char* get_next_move(const char* json_data) {
    const char* result = "forward";

    cJSON* root = cJSON_Parse(json_data);
    if (!root) return "stop";

    cJSON* front = cJSON_GetObjectItem(root, "front");
    cJSON* left = cJSON_GetObjectItem(root, "left");
    cJSON* right = cJSON_GetObjectItem(root, "right");

    int is_front = front ? front->valueint : 0;
    int is_left = left ? left->valueint : 0;
    int is_right = right ? right->valueint : 0;

    // אם זוהו איומים נוספים נבדוק
    cJSON* enemy = cJSON_GetObjectItem(root, "enemy");
    cJSON* explosive = cJSON_GetObjectItem(root, "explosive");
    cJSON* language = cJSON_GetObjectItem(root, "language");

    int danger_detected = 0;
    if ((enemy && cJSON_GetArraySize(enemy) > 0) ||
        (explosive && cJSON_GetArraySize(explosive) > 0) ||
        (language && strcmp(language->valuestring, "hostile") == 0)) {
        danger_detected = 1;
    }

    // לוגיקת תנועה
    if (is_front || danger_detected) {
        if (!is_right) result = "right";
        else if (!is_left) result = "left";
        else result = "stop";
    } else {
        result = "forward";
    }

    cJSON_Delete(root);
    return result;
}
