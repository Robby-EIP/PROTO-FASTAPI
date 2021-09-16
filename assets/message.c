/*
** EPITECH PROJECT, 2021
** message.c
** File description:
** message.c
*/

#include "message.h"
#include "../../include/server.h"
#include "../str_to_word_array/str_to_word_array.h"
#include <stdio.h>

int send_message(int socket, char *status_code, char *msg)
{
    if (dprintf(socket, "%s %s\r\n", status_code, msg) < 0)
        return ERROR;
    return SUCCESS;
}

int send_message_path(int socket, char *status_code, char *msg)
{
    if (dprintf(socket, "%s \"%s\"\r\n", status_code, msg) < 0)
        return ERROR;
    return SUCCESS;
}

char **read_message(int socket)
{
    char *buffer = NULL;
    FILE *file = fdopen(socket, "r");
    size_t length = 0;
    int len = 0;
    char **tab = NULL;

    len = getline(&buffer, &length, file);
    if (len == -1)
        buffer = "";
    tab = str_to_word_array(buffer, " ");
    (len != -1) ? free(buffer) : 0;
    if (tab != NULL)
        printf("tab[0] == '%s'\n", tab[0]);
    else
        printf("tab was nul\n");

    return tab;
}