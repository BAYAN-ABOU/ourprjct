#include <stdio.h>
#include <string.h>
#include <winsock2.h>

#pragma comment(lib,"ws2_32.lib")
#define BUFFER 1024

unsigned short crc16(const char *data) {
    unsigned short crc = 0xFFFF;
    while (*data) {
        crc ^= (*data++) << 8;
        for (int i=0;i<8;i++)
            crc = (crc & 0x8000) ? (crc<<1)^0x1021 : crc<<1;
    }
    return crc;
}

void build_packet(char *packet, const char *data) {
    sprintf(packet,"%s|CRC16|%04X",data,crc16(data));
}

void parse_packet(char *packet) {
    char d[BUFFER], m[50], c[50];
    sscanf(packet,"%[^|]|%[^|]|%s",d,m,c);
    printf("%s\n[Method: %s | Control: %s]\n\n",d,m,c);
}

int main() {
    WSADATA wsa;
    SOCKET sock;
    struct sockaddr_in server;
    char buffer[BUFFER], packet[BUFFER];

    WSAStartup(MAKEWORD(2,2),&wsa);
    sock = socket(AF_INET,SOCK_STREAM,0);

    server.sin_family = AF_INET;
    server.sin_port = htons(8080);
    server.sin_addr.s_addr = inet_addr("127.0.0.1");

    connect(sock,(struct sockaddr*)&server,sizeof(server));
    printf("Connected to server\n");

    while(1){
        int r = recv(sock,buffer,BUFFER-1,0);
        if(r<=0) break;
        buffer[r]='\0';
        parse_packet(buffer);

        if(strstr(buffer,"Enter cell number")){
            printf("Your move: ");
            fgets(buffer,BUFFER,stdin);
            buffer[strcspn(buffer,"\n")]=0;
            build_packet(packet,buffer);
            send(sock,packet,strlen(packet),0);
        }
    }
    closesocket(sock);
    WSACleanup();
    return 0;
}
