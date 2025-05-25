#!/bin/bash

# === BANNER SCP MIGRATE ===
clear
echo -e "\e[1;34m"
echo "███████╗ ██████╗██████╗     ███╗   ███╗██╗ ██████╗ ██████╗  █████╗ ████████╗███████╗"
echo "██╔════╝██╔════╝╚════██╗    ████╗ ████║██║██╔════╝ ██╔══██╗██╔══██╗╚══██╔══╝██╔════╝"
echo "█████╗  ██║      █████╔╝    ██╔████╔██║██║██║  ███╗██████╔╝███████║   ██║   █████╗  "
echo "██╔══╝  ██║     ██╔═══╝     ██║╚██╔╝██║██║██║   ██║██╔═══╝ ██╔══██║   ██║   ██╔══╝  "
echo "██║     ╚██████╗███████╗    ██║ ╚═╝ ██║██║╚██████╔╝██║     ██║  ██║   ██║   ███████╗"
echo "╚═╝      ╚═════╝╚══════╝    ╚═╝     ╚═╝╚═╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝   ╚═╝   ╚══════╝"
echo -e "\e[0m"
echo "                🔁 Script interactivo de migración con SCP"
echo ""

# === INPUT INTERACTIVO ===
read -p "📁 Ruta LOCAL del archivo o carpeta a copiar: " ORIGEN
read -p "👤 Usuario del servidor destino: " DESTINO_USUARIO
read -p "🌐 IP o dominio del servidor destino: " DESTINO_IP
read -p "📂 Ruta de destino en el servidor remoto: " DESTINO_RUTA
read -p "📦 Puerto SSH [Default 22]: " PUERTO_SSH

# Valor por defecto si se deja vacío
PUERTO_SSH=${PUERTO_SSH:-22}

# === COMPROBACIÓN Y EJECUCIÓN ===
echo ""
echo "🔄 Iniciando la transferencia con SCP..."
scp -P "$PUERTO_SSH" -r "$ORIGEN" "$DESTINO_USUARIO@$DESTINO_IP:$DESTINO_RUTA"

# === RESULTADO ===
if [ $? -eq 0 ]; then
    echo -e "\n✅ \e[1;32mTransferencia completada con éxito.\e[0m"
else
    echo -e "\n❌ \e[1;31mError durante la transferencia.\e[0m"
fi
