#!/bin/bash

# Değişkenler
APP_NAME="kainat-eczanesi"
VERSION="1.0.0"
DEB_DIR="${APP_NAME}_${VERSION}"

echo "📦 Paketleme işlemi başlıyor: $APP_NAME"

# 1. Klasör Yapısını Oluştur
mkdir -p $DEB_DIR/usr/bin
mkdir -p $DEB_DIR/usr/share/$APP_NAME
mkdir -p $DEB_DIR/usr/share/applications
mkdir -p $DEB_DIR/usr/share/icons/hicolor/256x256/apps
mkdir -p $DEB_DIR/DEBIAN

# 2. Dosyaları Kopyala
cp main.py $DEB_DIR/usr/share/$APP_NAME/
cp *.json $DEB_DIR/usr/share/$APP_NAME/ 2>/dev/null
cp icon.png $DEB_DIR/usr/share/icons/hicolor/256x256/apps/$APP_NAME.png

# 3. Çalıştırılabilir Başlatıcı Oluştur
cat <<EOF > $DEB_DIR/usr/bin/$APP_NAME
#!/bin/bash
cd /usr/share/$APP_NAME
python3 main.py "\$@"
EOF
chmod +x $DEB_DIR/usr/bin/$APP_NAME

# 4. Control Dosyası (Paket Bilgileri)
cat <<EOF > $DEB_DIR/DEBIAN/control
Package: $APP_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Maintainer: Mobilturka
Depends: python3, python3-pyqt6
Description: Kainat Eczanesi - Bitkisel Şifa Rehberi.
 Pardus 25 için geliştirilmiş bitki ve fayda sorgulama uygulaması.
EOF

# 5. Masaüstü Kısayolu (.desktop)
cat <<EOF > $DEB_DIR/usr/share/applications/$APP_NAME.desktop
[Desktop Entry]
Name=Kainat Eczanesi
Comment=Bitkisel Şifa Rehberi
Exec=$APP_NAME
Icon=$APP_NAME
Terminal=false
Type=Application
Categories=Education;
EOF

# 6. Paketi Oluştur
dpkg-deb --build $DEB_DIR

echo "✅ İşlem Tamamlandı: ${DEB_DIR}.deb oluşturuldu."