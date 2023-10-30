#include <time.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>
#include <wiringPi.h>
//log
#include <stdarg.h>
//#include <syslog.h>

#define START_HOUR 10
#define START_HOUR_1 22
#define END_SEC    15

#define AUTO_WATER_TRIG 4

void LOG(const char* ms, ... )  
{  
	char wzLog[1024] = {0};  
	char buffer[1024] = {0};  
	va_list args;  
	va_start(args, ms);  
	vsprintf( wzLog ,ms,args);  
	va_end(args);  

	time_t now;  
	time(&now);  
	struct tm *local;  
	local = localtime(&now);  
	printf("%04d-%02d-%02d %02d:%02d:%02d %s\n", local->tm_year+1900, local->tm_mon+1,  
		local->tm_mday, local->tm_hour, local->tm_min, local->tm_sec,  
		wzLog);  
	sprintf(buffer,"%04d-%02d-%02d %02d:%02d:%02d %s\n", local->tm_year+1900, local->tm_mon+1,  
		local->tm_mday, local->tm_hour, local->tm_min, local->tm_sec,  
		wzLog);  
	FILE* file = fopen("log.log","a+");  
	fwrite(buffer,1,strlen(buffer),file);  
	fclose(file);  

	//syslog(LOG_INFO,wzLog);  
	return ;  
}  

int main()
{
	time_t timer;
	struct tm *local_time;
	time_t first,second;	
	double difTime;
	int nHour =0;
	bool bHasStart=false;

	LOG("%s","************************************\n");
	LOG("%s","最右边1排，第1脚接继电器VCC，14脚-GND，16脚-IN\n");
	LOG("%s","2-VCC,14-GND,16-IN\n");

	wiringPiSetup();
	pinMode (AUTO_WATER_TRIG, OUTPUT);

	while(1)
	{

		time(&timer);
		local_time=localtime(&timer);
		//test
		nHour = local_time->tm_hour;
		//nHour = local_time->tm_min;
		//nHour = local_time->tm_sec;
		//printf("sec:%02d\n",nHour);

		if((nHour == START_HOUR || nHour == START_HOUR_1) && !bHasStart)
		{
			bHasStart = true;
			LOG("%s","-------------------------------\n");   
			LOG("Local time is:%s",asctime(local_time));	
			LOG("hour:%02d\n",nHour);

			//打开继电器
			digitalWrite(AUTO_WATER_TRIG,HIGH);
			LOG("%s","start...\n");

			first=time(NULL);
			sleep(END_SEC);
			second=time(NULL);
			difTime = difftime(second,first);

			//关闭继电器
			digitalWrite(AUTO_WATER_TRIG,LOW);
			LOG("diff:%f seconds\n",difTime);
			LOG("%s","close...\n");
			LOG("%s","-------------------------------\n");

		}
		else if((nHour != START_HOUR) &&  (nHour != START_HOUR_1))
			bHasStart = false;

		sleep(10);
		//usleep(1000000);

	}

	return 0;
}
