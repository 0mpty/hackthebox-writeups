// hack the box - HILLarious 
#include <iostream>
#include <cstring>
#include <filesystem>
#include <sstream>
#include <fstream>
#include <chrono>
#include <vector>
#include <string_view>

using namespace std;

class Decoder {
private:
    vector<int> param_1 = vector<int>(8);
    vector<int> param_2 = vector<int>(4);
    unsigned long long constant = 0xcbf29ce484222325ULL;

    void changeConstant(time_t time) {
        int count = 8;
        do {
            int value = time & 0xff;
            time = time >> 8;
            constant = (constant ^ value) * 0x100000001b3ULL;
            count--;
        } while(count != 0);
        constant = constant ^ 0xdeadbeefcafebabeULL;

        cout<< "[+] The main constant is got\n";
    }

    void createParam_1() {
        int count = 0;
        do {
           int shift = (count * 8 & 0x3f);
           param_1[count] = (constant >> shift) & 0xff;
           count++;
        } while(count != 8);

        cout<< "[+] The first secret array is got\n";
    }

    void createParam_2() {
        unsigned long long v = constant * 0x5851f42d4c957f2dULL + 0x6c576fac43fd007cULL;

        long long value = v;
        long long value2 = value * 0x4c957f2d + 0xf767814f;
        long long value3 = value2 & 0xff;
        value = (value & 0xff) | 1;
        value2 = value2 * 0x4c957f2d + 0xf767814f;
        long long value4 = value2 & 0xff;
        value2 = ((value2 * 0x4c957f2d + 0xf767814f) & 0xff) | 1;

        long long global_value = ((value2 << 8 | value4) << 8 | value3) << 8 | value;

        param_2[3] = (global_value >> 24) & 0xff;
        param_2[2] = (global_value >> 16) & 0xff;
        param_2[1] = (global_value >> 8) & 0xff;
        param_2[0] = global_value & 0xff;
        if ((value * value2 - value3 * value4) == 0) {
            param_2[0] = ((v | 1) + 2) & 0xff;
        }

        cout<< "[+] The second secret array is got\n";
    }

    int modInverse(int a, int m) {
        a = a % m;
        for (int x = 1; x < m; x++) {
            if ((a * x) % m == 1) return x;
        }

        return 1;
    }

    void decoding(string& enc, string& dec, int size) {
        for (int count = 0; count < size; count += 2) {
            int value1 = param_1[count & 7] ^ enc[count];
            int value2 = param_1[(count + 1) & 7] ^ enc[count + 1];

            int p1 = param_2[0], p2 = param_2[1], p3 = param_2[2], p4 = param_2[3];
            int delta = (p1 * p4 - p2 * p3) & 0xff;
            int inv = modInverse(delta, 256);

            char x = ((value1 * p4 - p2 * value2) * inv) & 0xff;
            char y = ((p1 * value2 - value1 * p3) * inv) & 0xff;

            dec[count] = x;
            dec[count + 1] = y;
        }

    } 

    string startDecoding(string& enc, int size, time_t time){
        string decodeText(size, ' ');

        changeConstant(time);
        createParam_1();
        createParam_2();

        decoding(enc, decodeText, size);

        return decodeText;
    }

public:
     time_t getTime(const char* fileName) {
        filesystem::path filePath(fileName);

        auto ftime = filesystem::last_write_time(filePath);
        auto sys_time = chrono::file_clock::to_sys(ftime);

        time_t time = chrono::system_clock::to_time_t(sys_time);

        return time;
    }

    int writeDecodedText(string& dec, const char* fileName) {
	size_t len = strlen(fileName);
	size_t new_len = (len > 4) ? (len - 4) : 0;
	string_view slice(fileName, new_len);

	string decodeFileName = string(slice) + ".dec";
	ofstream out(decodeFileName);

        if (! out.is_open()) {
            cerr << "[-] Error: The file cannot been created\n";
            return 0;
        }

        out << dec;
        out.close();

        cout << "[+] " << decodeFileName << " succesfully created!!!\n";
        
        return 1;
    }

    string readFile(const char* fileName) {
        ifstream in(fileName, ios::binary);
        stringstream buffer;
        string encryptedText = "";

        int textLen = 0;
        if (in.is_open()) {
            buffer << in.rdbuf();
            encryptedText = buffer.str();
            textLen = encryptedText.length();
            if (textLen > 20) {
                encryptedText = encryptedText.substr(20);
                textLen -= 20;
            }else {
                cerr << "[-] Error: Data was incorrect\n";
                return "";
            }
        } else {
        	cerr << "[-] Error: Could not open " << fileName << endl;
		return "";
        }

        time_t time = getTime(fileName);
        string decodedText = startDecoding(encryptedText, textLen, time);
        writeDecodedText(decodedText, fileName);
	return "[+] Finish!\n";
    }
};

int main(int argc, char* argv[]) {
    if (argc != 3){
        cerr << "[-] Error: Not enough args\n"; 
        return 1;
    }
    if (string(argv[1]) != "decode") {
        cerr << "[-] Usage: ./DeHill decode <YourFileName>\n";
        return 1;
    }
    if (! filesystem::exists(argv[2])) {
        cerr << "[-] The file " << argv[2] << " does not exist\n";
        return 1;
    }

    Decoder user;

    string end_text = user.readFile(argv[2]);

    cout << end_text;

    return 0;
}
