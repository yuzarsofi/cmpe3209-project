/* Yusuf Kemal AKYILDIZ, SID 5001230017 (programda son 9 hane: 1230017), G3 */
const int SID = 1230017;  // 5001230017 > 2^31-1 (int siniri) oldugu icin son 9 hane kullanildi
int a[41];
unsigned int checksum = 0;
int decrypt_ok = 0;

unsigned int rotl(unsigned int val) {
    return (val << 1) | (val >> 31);
}

int main() {
    // K anahtarini hesapla
    unsigned int K = SID % 256;
    if (K == 0) {
        K = 0xA5;
    }

    // Diziyi LCG ile doldur
    unsigned int x = SID;
    for (int i = 0; i < 41; i++) {
        x = 1664525 * x + 1013904223;
        a[i] = ((x >> 16) % 26) + 65;
    }

    // Birinci gecis: sifrele ve checksum hesapla
    for (int i = 0; i < 41; i++) {
        a[i] = a[i] ^ K;
        checksum = rotl(checksum) + a[i];
    }

    // Ikinci gecis: coz ve orijinalle karsilastir
    x = SID;
    int flag = 1;
    for (int i = 0; i < 41; i++) {
        x = 1664525 * x + 1013904223;
        int v = ((x >> 16) % 26) + 65;
        a[i] = a[i] ^ K;
        if (a[i] != v) {
            flag = 0;
        }
    }

    decrypt_ok = flag;
    return 0;
}
