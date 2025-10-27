#ifndef CSVLOGGER_H
#define CSVLOGGER_H

#include <string>
#include <fstream>
#include <ctime>
#include <iomanip>
#include <chrono>

class CSVLogger {
    private:
        std::ofstream file;
        std::string path;
        bool writtenHeader;

    public:
        CSVLogger(const std::string& fileName);
        ~CSVLogger();

        void writeHeader(const std::string& header);
        void writeLine(float temperature, float pressure, float humidity);
};

#endif