#!/bin/bash

# Folders
SOURCE_FOLDER="/srv/outline/" # make sure your ouline is here 
BACKUP_FOLDER="/tmp/backup_outline/"
ARCHIVE_NAME="backup_outline_$(date +'%Y%m%d').tar.gz"
BOT_TOKEN="71111113:AAmdansfuanjn3j12adaPeRyKe_k"  # Your Bot Token from Botfather
CHAT_ID="-4111111111"      # Telegram chat_id

echo "$(date +'%Y-%m-%d %H:%M:%S') - Starting backup of Outline Wiki" >> $LOG_FILE
curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="Starting backup of Outline  Wiki $(date +'%Y-%m-%d %H:%M:%S')"

tar -czf /tmp/$ARCHIVE_NAME -C $SOURCE_FOLDER .

if [ $? -ne 0 ]; then
  echo "$(date +'%Y-%m-%d %H:%M:%S') - Error while trying to arvhive your data" >> $LOG_FILE
  curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
      -d chat_id="$CHAT_ID" \
      -d text="Error while trying to arvhive your data $(date +'%Y-%m-%d %H:%M:%S')"
  exit 1
fi

# 2. Split files to 45 mbs
split -b 45M /tmp/$ARCHIVE_NAME /tmp/backup_part_

for PART in /tmp/backup_part_*; do
    curl -F chat_id="$CHAT_ID" -F document=@"$PART" https://api.telegram.org/bot$BOT_TOKEN/sendDocument
    if [ $? -ne 0 ]; then
        echo "$(date +'%Y-%m-%d %H:%M:%S') - Error sending $PART to Telegram" >> $LOG_FILE
        curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
            -d chat_id="$CHAT_ID" \
            -d text="Error sending $PART to Telegram $(date +'%Y-%m-%d %H:%M:%S')"
        exit 1
    fi
    sleep 1  
done


rm /tmp/backup_part_*
rm /tmp/$ARCHIVE_NAME

echo "$(date +'%Y-%m-%d %H:%M:%S') - Backup Done " >> $LOG_FILE
curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="Backup Done $(date +'%Y-%m-%d %H:%M:%S')"
