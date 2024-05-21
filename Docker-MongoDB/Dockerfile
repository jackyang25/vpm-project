# Use an official MongoDB image
FROM mongo

# Set the working directory in the container
WORKDIR /data

# Copy the CSV file and the Bash script into the container
COPY train.csv /data/train.csv
COPY import_script.sh /data/import_script.sh

# Make the import script executable
RUN chmod +x /data/import_script.sh

# Run the import script when the container starts
CMD ["./import_script.sh"]