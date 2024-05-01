import xml.etree.ElementTree as ET

class KWICPlus:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.data = self.load_data()

    def load_data(self):
        try:
            tree = ET.parse(self.xml_file)
            root = tree.getroot()
            data = []
            for entry in root.findall('entry'):
                descriptor = entry.find('descriptor').text
                url = entry.find('url').text
                data.append((descriptor, url))
            return data
        except (ET.ParseError, FileNotFoundError) as e:
            print(f"Error loading data from XML file: {e}")
            return []

    def circular_shift(self, descriptor):
        words = descriptor.split()
        shifts = []
        for i in range(len(words)):
            shift = ' '.join(words[i:] + words[:i])
            shifts.append(shift)
        return shifts

    def filter_noise_words(self, descriptor):
        noise_words = ["a", "an", "the", "and", "or", "of", "to", "be", "is", "in", "out", "by", "as", "at", "off"]
        words = descriptor.split()
        filtered_words = [word for word in words if word.lower() not in noise_words]
        return ' '.join(filtered_words)

    def search_url(self, keywords):
        matching_urls = []
        for descriptor, url in self.data:
            circular_shifts = self.circular_shift(descriptor)
            for shift in circular_shifts:
                filtered_shift = self.filter_noise_words(shift)
                if all(keyword.lower() in filtered_shift.lower() for keyword in keywords):
                    matching_urls.append({'descriptor': filtered_shift, 'url': url})
        return matching_urls

    def add_entry(self, descriptor, url):
        try:
            # Open the file in append mode
            with open(self.xml_file, 'a') as f:
                # Create a new entry element
                new_entry = ET.Element('entry')

                # Create descriptor and URL elements under the entry
                descriptor_elem = ET.SubElement(new_entry, 'descriptor')
                descriptor_elem.text = descriptor

                url_elem = ET.SubElement(new_entry, 'url')
                url_elem.text = url

                # Write the new entry to the file
                f.write(ET.tostring(new_entry).decode() + '\n')

            print("Entry added successfully.")
        except Exception as e:
            print(f"Error adding entry to XML file: {e}")

if __name__ == "__main__":
    kwic_plus = KWICPlus('kwic_data.xml')
    
    # Get user input for descriptor and URL
    descriptor = input("Enter descriptor: ")
    url = input("Enter URL: ")
    
    # Add the entry to the XML file
    kwic_plus.add_entry_to_xml(descriptor, url)
