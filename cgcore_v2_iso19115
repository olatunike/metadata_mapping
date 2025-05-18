# metadata_mapping.py
# Script to map CGCore v2 metadata to ISO 19115

class MetadataMapper:
    def __init__(self):
        # Define mapping dictionary: CGCore v2 to ISO 19115
        self.mapping = {
            'title': 'identificationInfo/MD_DataIdentification/citation/CI_Citation/title',
            'creator': 'identificationInfo/MD_DataIdentification/citation/CI_Citation/citedResponsibleParty/CI_ResponsibleParty/individualName',
            'subject': 'identificationInfo/MD_DataIdentification/topicCategory',
            'description': 'identificationInfo/MD_DataIdentification/abstract',
            'publisher': 'identificationInfo/MD_DataIdentification/citation/CI_Citation/citedResponsibleParty/CI_ResponsibleParty/organisationName',
            'date': 'identificationInfo/MD_DataIdentification/citation/CI_Citation/date/CI_Date/date',
            'type': 'identificationInfo/MD_DataIdentification/resourceFormat',
            'format': 'distributionInfo/MD_Distribution/transferOptions/MD_DigitalTransferOptions/onLine/CI_OnlineResource/applicationProfile',
            'identifier': 'identificationInfo/MD_DataIdentification/citation/CI_Citation/identifier/MD_Identifier/code',
            'language': 'identificationInfo/MD_DataIdentification/language',
            'spatial_extent': 'identificationInfo/MD_DataIdentification/extent/EX_Extent/geographicElement/EX_GeographicBoundingBox',
            'temporal_extent': 'identificationInfo/MD_DataIdentification/extent/EX_Extent/temporalElement/EX_TemporalExtent/extent'
        }
        
        # Reverse mapping for ISO 19115 to CGCore v2
        self.reverse_mapping = {v: k for k, v in self.mapping.items()}

    def cgcore_to_iso19115(self, cgcore_metadata):
        """
        Convert CGCore v2 metadata to ISO 19115 structure
        Args:
            cgcore_metadata (dict): Dictionary containing CGCore metadata
        Returns:
            dict: ISO 19115 structured metadata
        """
        iso_metadata = {}
        
        for cgcore_field, value in cgcore_metadata.items():
            if cgcore_field in self.mapping:
                iso_path = self.mapping[cgcore_field]
                # Create nested structure for ISO 19115 path
                current = iso_metadata
                path_parts = iso_path.split('/')
                
                # Build nested dictionary structure
                for i, part in enumerate(path_parts[:-1]):
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                
                # Set the value at the final path component
                current[path_parts[-1]] = value
                
        return iso_metadata

    def iso19115_to_cgcore(self, iso_metadata):
        """
        Convert ISO 19115 metadata to CGCore v2 structure
        Args:
            iso_metadata (dict): Dictionary containing ISO 19115 metadata
        Returns:
            dict: CGCore v2 structured metadata
        """
        cgcore_metadata = {}
        
        def traverse_iso_dict(current_dict, current_path=''):
            for key, value in current_dict.items():
                new_path = f"{current_path}/{key}" if current_path else key
                
                if isinstance(value, dict):
                    traverse_iso_dict(value, new_path)
                else:
                    if new_path in self.reverse_mapping:
                        cgcore_field = self.reverse_mapping[new_path]
                        cgcore_metadata[cgcore_field] = value
        
        traverse_iso_dict(iso_metadata)
        return cgcore_metadata

def main():
    # Example usage
    mapper = MetadataMapper()
    
    # Sample CGCore metadata
    cgcore_sample = {
        'title': 'Sample Dataset',
        'creator': 'John Doe',
        'subject': 'Environment',
        'description': 'A sample geospatial dataset',
        'publisher': 'Example Org',
        'date': '2023-01-01',
        'identifier': 'dataset-001',
        'language': 'eng',
        'spatial_extent': '-180,-90,180,90'
    }
    
    # Convert to ISO 19115
    iso_result = mapper.cgcore_to_iso19115(cgcore_sample)
    print("CGCore to ISO 19115:")
    print(iso_result)
    
    # Convert back to CGCore
    cgcore_result = mapper.iso19115_to_cgcore(iso_result)
    print("\nISO 19115 back to CGCore:")
    print(cgcore_result)

if __name__ == "__main__":
    main()
