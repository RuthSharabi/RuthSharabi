#include <stdio.h>
#include <string.h>
#include <stdbool.h>

void parse_input(char *input, bool *front, bool *left, bool *right) {
    sscanf(input, "front=%d;left=%d;right=%d", 
           (int*)front, (int*)left, (int*)right);
}

int main() {
    char input[100];
    bool front = false, left = false, right = false;

    while (fgets(input, sizeof(input), stdin)) {
        parse_input(input, &front, &left, &right);

        // זיהוי מבוי סתום
        if (front && left && right) {
            printf("DEAD_END_TURN_AROUND\n");
        }
        // אלגוריתם תמיד ימינה
        else if (!right) {
            printf("TURN_RIGHT\n");
        }
        else if (!front) {
            printf("GO_FORWARD\n");
        }
        else if (!left) {
            printf("TURN_LEFT\n");
        }
        else {
            printf("WAIT_OR_BACK\n"); // רק למקרה שלא ברור
        }

        fflush(stdout);
    }

    return 0;
}
