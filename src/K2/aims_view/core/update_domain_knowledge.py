"""
Dynamic Domain Knowledge Updater
Manually updates domain knowledge by querying the database for all code/name field pairs
Run this script manually whenever you want to refresh the domain knowledge with latest database values
"""

import json
import os
from datetime import datetime
from pathlib import Path
import sys

# Add project root to path
project_root = str(Path(__file__).parent.parent.parent.parent.parent)
sys.path.insert(0, project_root)

from src.K2.aims_view.database.database import DomainKnowledge


class DomainKnowledgeUpdater(DomainKnowledge):
    """Dynamically update domain knowledge from database"""
    
    def __init__(self):
        super().__init__()
        self.updated_knowledge = {}
        self.update_timestamp = datetime.now().isoformat()
    
    def fetch_branches(self):
        """Get all branches with IDs and names"""
        print("📊 Fetching branches...")
        query = """
        SELECT DISTINCT DOC_BRANCH, DOC_BRANCH_NAME 
        FROM insmv.AIMS_ALL_DATA 
        WHERE DOC_BRANCH IS NOT NULL AND DOC_BRANCH_NAME IS NOT NULL
        ORDER BY DOC_BRANCH
        """
        df = self._safe_execute_query(query)
        
        branches = []
        for _, row in df.iterrows():
            branches.append({
                "id": str(row['DOC_BRANCH']),
                "name": str(row['DOC_BRANCH_NAME'])
            })
        
        print(f"   ✅ Found {len(branches)} branches")
        return branches
    
    def fetch_offices(self):
        """Get all offices with IDs and names"""
        print("📊 Fetching offices...")
        query = """
        SELECT DISTINCT DOC_OFFICE, DOC_OFFICE_NAME, DOC_BRANCH, DOC_BRANCH_NAME
        FROM insmv.AIMS_ALL_DATA 
        WHERE DOC_OFFICE IS NOT NULL AND DOC_OFFICE_NAME IS NOT NULL
        ORDER BY DOC_BRANCH, DOC_OFFICE
        """
        df = self._safe_execute_query(query)
        
        offices = []
        for _, row in df.iterrows():
            offices.append({
                "id": str(row['DOC_OFFICE']),
                "name": str(row['DOC_OFFICE_NAME']),
                "branch_id": str(row['DOC_BRANCH']),
                "branch_name": str(row['DOC_BRANCH_NAME'])
            })
        
        print(f"   ✅ Found {len(offices)} offices")
        return offices
    
    def fetch_major_insurance_types(self):
        """Get all major insurance types (lines of business)"""
        print("📊 Fetching major insurance types (lines of business)...")
        query = """
        SELECT DISTINCT DOC_MAJ_INS_TYPE, DOC_MAJ_NAME 
        FROM insmv.AIMS_ALL_DATA 
        WHERE DOC_MAJ_INS_TYPE IS NOT NULL AND DOC_MAJ_NAME IS NOT NULL
        ORDER BY DOC_MAJ_INS_TYPE
        """
        df = self._safe_execute_query(query)
        
        types = []
        for _, row in df.iterrows():
            types.append({
                "code": str(row['DOC_MAJ_INS_TYPE']),
                "name": str(row['DOC_MAJ_NAME'])
            })
        
        print(f"   ✅ Found {len(types)} major insurance types")
        return types
    
    def fetch_minor_insurance_types(self):
        """Get all minor insurance types (products/subclasses)"""
        print("📊 Fetching minor insurance types (products)...")
        query = """
        SELECT DISTINCT DOC_MIN_INS_TYPE, DOC_MIN_NAME, DOC_MAJ_INS_TYPE, DOC_MAJ_NAME
        FROM insmv.AIMS_ALL_DATA 
        WHERE DOC_MIN_INS_TYPE IS NOT NULL AND DOC_MIN_NAME IS NOT NULL
        ORDER BY DOC_MAJ_INS_TYPE, DOC_MIN_INS_TYPE
        """
        df = self._safe_execute_query(query)
        
        types = []
        for _, row in df.iterrows():
            types.append({
                "code": str(row['DOC_MIN_INS_TYPE']),
                "name": str(row['DOC_MIN_NAME']),
                "major_type_code": str(row['DOC_MAJ_INS_TYPE']),
                "major_type_name": str(row['DOC_MAJ_NAME'])
            })
        
        print(f"   ✅ Found {len(types)} minor insurance types")
        return types
    
    def fetch_business_types(self):
        """Get all business types"""
        print("📊 Fetching business types...")
        query = """
        SELECT DISTINCT DOC_BUS_TYPE, DOC_BUS_NAME 
        FROM insmv.AIMS_ALL_DATA 
        WHERE DOC_BUS_TYPE IS NOT NULL AND DOC_BUS_NAME IS NOT NULL
        ORDER BY DOC_BUS_TYPE
        """
        df = self._safe_execute_query(query)
        
        types = []
        for _, row in df.iterrows():
            types.append({
                "code": str(row['DOC_BUS_TYPE']),
                "name": str(row['DOC_BUS_NAME'])
            })
        
        print(f"   ✅ Found {len(types)} business types")
        return types
    
    def fetch_accident_types(self):
        """Get all accident types"""
        print("📊 Fetching accident types...")
        query = """
        SELECT DISTINCT CLAIM_ACC_TYPE, CLAIM_ACC_TYPE_NAME 
        FROM insmv.AIMS_ALL_DATA 
        WHERE CLAIM_ACC_TYPE IS NOT NULL AND CLAIM_ACC_TYPE_NAME IS NOT NULL
        ORDER BY CLAIM_ACC_TYPE
        """
        df = self._safe_execute_query(query)
        
        types = []
        for _, row in df.iterrows():
            types.append({
                "code": str(row['CLAIM_ACC_TYPE']),
                "name": str(row['CLAIM_ACC_TYPE_NAME'])
            })
        
        print(f"   ✅ Found {len(types)} accident types")
        return types
    
    def fetch_vehicle_makes(self):
        """Get all vehicle makes"""
        print("📊 Fetching vehicle makes...")
        query = """
        SELECT DISTINCT DOC_MAKE, DOC_MAKE_NAME 
        FROM insmv.AIMS_ALL_DATA 
        WHERE DOC_MAKE IS NOT NULL AND DOC_MAKE_NAME IS NOT NULL
        ORDER BY DOC_MAKE_NAME
        """
        df = self._safe_execute_query(query)
        
        makes = []
        for _, row in df.iterrows():
            makes.append({
                "code": str(row['DOC_MAKE']),
                "name": str(row['DOC_MAKE_NAME'])
            })
        
        print(f"   ✅ Found {len(makes)} vehicle makes")
        return makes
    
    def fetch_vehicle_models(self):
        """Get all vehicle models with their makes"""
        print("📊 Fetching vehicle models...")
        query = """
        SELECT DISTINCT DOC_MAKE, DOC_MAKE_NAME, DOC_MODEL 
        FROM insmv.AIMS_ALL_DATA 
        WHERE DOC_MODEL IS NOT NULL AND DOC_MAKE IS NOT NULL
        ORDER BY DOC_MAKE_NAME, DOC_MODEL
        """
        df = self._safe_execute_query(query)
        
        models = []
        for _, row in df.iterrows():
            models.append({
                "model_name": str(row['DOC_MODEL']),
                "make_code": str(row['DOC_MAKE']),
                "make_name": str(row['DOC_MAKE_NAME'])
            })
        
        print(f"   ✅ Found {len(models)} vehicle models")
        return models
    
    def fetch_plate_types(self):
        """Get all plate types"""
        print("📊 Fetching plate types...")
        query = """
        SELECT DISTINCT DOC_PLATE_TYPE, DOC_PLATE_TYPE_NAME 
        FROM insmv.AIMS_ALL_DATA 
        WHERE DOC_PLATE_TYPE IS NOT NULL AND DOC_PLATE_TYPE_NAME IS NOT NULL
        ORDER BY DOC_PLATE_TYPE
        """
        df = self._safe_execute_query(query)
        
        types = []
        for _, row in df.iterrows():
            types.append({
                "code": str(row['DOC_PLATE_TYPE']),
                "name": str(row['DOC_PLATE_TYPE_NAME'])
            })
        
        print(f"   ✅ Found {len(types)} plate types")
        return types
    
    def fetch_plate_colors(self):
        """Get all plate colors"""
        print("📊 Fetching plate colors...")
        query = """
        SELECT DISTINCT DOC_PLATE_COLOR, DOC_COLOR_NAME 
        FROM insmv.AIMS_ALL_DATA 
        WHERE DOC_PLATE_COLOR IS NOT NULL AND DOC_COLOR_NAME IS NOT NULL
        ORDER BY DOC_PLATE_COLOR
        """
        df = self._safe_execute_query(query)
        
        colors = []
        for _, row in df.iterrows():
            colors.append({
                "code": str(row['DOC_PLATE_COLOR']),
                "name": str(row['DOC_COLOR_NAME'])
            })
        
        print(f"   ✅ Found {len(colors)} plate colors")
        return colors
    
    def fetch_body_types(self):
        """Get all body types"""
        print("📊 Fetching body types...")
        query = """
        SELECT DISTINCT DOC_BODY_TYPE, DOC_BODY_NAME 
        FROM insmv.AIMS_ALL_DATA 
        WHERE DOC_BODY_TYPE IS NOT NULL AND DOC_BODY_NAME IS NOT NULL
        ORDER BY DOC_BODY_TYPE
        """
        df = self._safe_execute_query(query)
        
        types = []
        for _, row in df.iterrows():
            types.append({
                "code": str(row['DOC_BODY_TYPE']),
                "name": str(row['DOC_BODY_NAME'])
            })
        
        print(f"   ✅ Found {len(types)} body types")
        return types
    
    def fetch_cylinder_types(self):
        """Get all cylinder types"""
        print("📊 Fetching cylinder types...")
        query = """
        SELECT DISTINCT DOC_CYLENDER, DOC_CYLENDER_NAME 
        FROM insmv.AIMS_ALL_DATA 
        WHERE DOC_CYLENDER IS NOT NULL AND DOC_CYLENDER_NAME IS NOT NULL
        ORDER BY DOC_CYLENDER
        """
        df = self._safe_execute_query(query)
        
        types = []
        for _, row in df.iterrows():
            types.append({
                "code": str(row['DOC_CYLENDER']),
                "name": str(row['DOC_CYLENDER_NAME'])
            })
        
        print(f"   ✅ Found {len(types)} cylinder types")
        return types
    
    def fetch_data_sources(self):
        """Get all data sources"""
        print("📊 Fetching data sources...")
        query = """
        SELECT DISTINCT DOC_SOURCE_NAME 
        FROM insmv.AIMS_ALL_DATA 
        WHERE DOC_SOURCE_NAME IS NOT NULL
        ORDER BY DOC_SOURCE_NAME
        """
        df = self._safe_execute_query(query)
        
        sources = [str(row['DOC_SOURCE_NAME']) for _, row in df.iterrows()]
        
        print(f"   ✅ Found {len(sources)} data sources")
        return sources
    
    def fetch_agents_brokers(self):
        """Get all agents/brokers"""
        print("📊 Fetching agents/brokers...")
        query = """
        SELECT DISTINCT DOC_AGENT_NAME 
        FROM insmv.AIMS_ALL_DATA 
        WHERE DOC_AGENT_NAME IS NOT NULL
        ORDER BY DOC_AGENT_NAME
        """
        df = self._safe_execute_query(query)
        
        agents = [str(row['DOC_AGENT_NAME']) for _, row in df.iterrows()]
        
        print(f"   ✅ Found {len(agents)} agents/brokers")
        return agents
    
    def fetch_payment_slip_types(self):
        """Get all payment slip types"""
        print("📊 Fetching payment slip types...")
        query = """
        SELECT DISTINCT PAY_SLIP_TYPE, PAY_SLIP_TYPE_NAME 
        FROM insmv.AIMS_ALL_DATA 
        WHERE PAY_SLIP_TYPE IS NOT NULL AND PAY_SLIP_TYPE_NAME IS NOT NULL
        ORDER BY PAY_SLIP_TYPE
        """
        df = self._safe_execute_query(query)
        
        types = []
        for _, row in df.iterrows():
            types.append({
                "code": str(row['PAY_SLIP_TYPE']),
                "name": str(row['PAY_SLIP_TYPE_NAME'])
            })
        
        print(f"   ✅ Found {len(types)} payment slip types")
        return types
    
    def fetch_claim_causes(self):
        """Get all claim causes"""
        print("📊 Fetching claim causes...")
        query = """
        SELECT DISTINCT CLAIM_CAUSE_OF_LOSS, CLAIM_CAUSE_NAME 
        FROM insmv.AIMS_ALL_DATA 
        WHERE CLAIM_CAUSE_OF_LOSS IS NOT NULL AND CLAIM_CAUSE_NAME IS NOT NULL
        ORDER BY CLAIM_CAUSE_OF_LOSS
        """
        df = self._safe_execute_query(query)
        
        causes = []
        for _, row in df.iterrows():
            causes.append({
                "code": str(row['CLAIM_CAUSE_OF_LOSS']),
                "name": str(row['CLAIM_CAUSE_NAME'])
            })
        
        print(f"   ✅ Found {len(causes)} claim causes")
        return causes
    
    def fetch_all_dynamic_data(self):
        """Fetch all dynamic data from database"""
        print("\n" + "="*70)
        print("🚀 DYNAMIC DOMAIN KNOWLEDGE UPDATE STARTED")
        print("="*70 + "\n")
        
        self.updated_knowledge = {
            "metadata": {
                "last_updated": self.update_timestamp,
                "update_type": "manual",
                "source": "AIMS_ALL_DATA table"
            },
            "dynamic_data": {
                "branches": self.fetch_branches(),
                "offices": self.fetch_offices(),
                "major_insurance_types": self.fetch_major_insurance_types(),
                "minor_insurance_types": self.fetch_minor_insurance_types(),
                "business_types": self.fetch_business_types(),
                "accident_types": self.fetch_accident_types(),
                "vehicle_makes": self.fetch_vehicle_makes(),
                "vehicle_models": self.fetch_vehicle_models(),
                "plate_types": self.fetch_plate_types(),
                "plate_colors": self.fetch_plate_colors(),
                "body_types": self.fetch_body_types(),
                "cylinder_types": self.fetch_cylinder_types(),
                "data_sources": self.fetch_data_sources(),
                "agents_brokers": self.fetch_agents_brokers(),
                "payment_slip_types": self.fetch_payment_slip_types(),
                "claim_causes": self.fetch_claim_causes()
            }
        }
        
        print("\n" + "="*70)
        print("✅ DYNAMIC DOMAIN KNOWLEDGE UPDATE COMPLETED")
        print("="*70 + "\n")
        
        return self.updated_knowledge
    
    def save_to_json(self, output_path: str = None):
        """Save updated knowledge to JSON file"""
        if output_path is None:
            # Save in the same directory as this script
            output_path = Path(__file__).parent / "dynamic_domain_knowledge.json"
        
        print(f"💾 Saving to: {output_path}")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.updated_knowledge, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved successfully!")
        print(f"📁 File location: {output_path}")
        return output_path
    
    def print_summary(self):
        """Print summary of updated knowledge"""
        print("\n" + "="*70)
        print("📊 DOMAIN KNOWLEDGE UPDATE SUMMARY")
        print("="*70)
        
        if not self.updated_knowledge:
            print("❌ No data updated yet. Run fetch_all_dynamic_data() first.")
            return
        
        dynamic_data = self.updated_knowledge.get("dynamic_data", {})
        
        print(f"\n⏰ Last Updated: {self.updated_knowledge['metadata']['last_updated']}")
        print(f"\n📈 Data Counts:")
        print(f"   • Branches: {len(dynamic_data.get('branches', []))}")
        print(f"   • Offices: {len(dynamic_data.get('offices', []))}")
        print(f"   • Major Insurance Types: {len(dynamic_data.get('major_insurance_types', []))}")
        print(f"   • Minor Insurance Types: {len(dynamic_data.get('minor_insurance_types', []))}")
        print(f"   • Business Types: {len(dynamic_data.get('business_types', []))}")
        print(f"   • Accident Types: {len(dynamic_data.get('accident_types', []))}")
        print(f"   • Vehicle Makes: {len(dynamic_data.get('vehicle_makes', []))}")
        print(f"   • Vehicle Models: {len(dynamic_data.get('vehicle_models', []))}")
        print(f"   • Plate Types: {len(dynamic_data.get('plate_types', []))}")
        print(f"   • Plate Colors: {len(dynamic_data.get('plate_colors', []))}")
        print(f"   • Body Types: {len(dynamic_data.get('body_types', []))}")
        print(f"   • Cylinder Types: {len(dynamic_data.get('cylinder_types', []))}")
        print(f"   • Data Sources: {len(dynamic_data.get('data_sources', []))}")
        print(f"   • Agents/Brokers: {len(dynamic_data.get('agents_brokers', []))}")
        print(f"   • Payment Slip Types: {len(dynamic_data.get('payment_slip_types', []))}")
        print(f"   • Claim Causes: {len(dynamic_data.get('claim_causes', []))}")
        
        print("\n" + "="*70 + "\n")


def main():
    """Main function to run the update"""
    print("\n" + "="*70)
    print("🎯 K2 DOMAIN KNOWLEDGE UPDATER")
    print("="*70 + "\n")
    
    try:
        # Initialize updater
        updater = DomainKnowledgeUpdater()
        
        # Fetch all dynamic data
        updated_knowledge = updater.fetch_all_dynamic_data()
        
        # Print summary
        updater.print_summary()
        
        # Save to JSON file
        output_file = updater.save_to_json()
        
        print("\n" + "="*70)
        print("🎉 SUCCESS! Domain knowledge has been updated")
        print("="*70)
        print(f"\n📝 Next Steps:")
        print(f"   1. Review the generated file: {output_file}")
        print(f"   2. Integrate this data into your agents as needed")
        print(f"   3. Run this script again whenever you want fresh data")
        print("\n" + "="*70 + "\n")
        
    except Exception as e:
        print("\n" + "="*70)
        print("❌ ERROR OCCURRED")
        print("="*70)
        print(f"\n{str(e)}")
        print("\n" + "="*70 + "\n")
        raise


if __name__ == "__main__":
    main()

