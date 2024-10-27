from asyncio import Event
import csv
from dataclasses import dataclass
from typing import Dict, List, Set
from collections import defaultdict

@dataclass
class Event:
    event_id: str
    title: str
    acronym: str
    project_code: str
    three_digit_code: str
    record_type: str

class EventProcessor:
    def __init__(self):
        self.events: Dict[str, Event] = {}
        self.parents_by_acronym: Dict[str, List[Event]] = defaultdict(list)
        self.children_by_acronym: Dict[str, List[Event]] = defaultdict(list)

    def load_csv(self, csv_content: str) -> None:
        """Load and parse CSV content into Event objects."""
        reader = csv.reader(csv_content.splitlines())
        next(reader)  # Skip header
        
        valid_rows = []  # List to store valid rows
        
        for row in reader:
            # Skip empty rows
            if not row or len(row) < 6:
                continue
                
            event = Event(
                event_id=row[0].strip(),           # Added strip()
                title=row[1].strip(),              # Added strip()
                acronym=row[2].strip(),            # Added strip()
                project_code=row[3].strip() if row[3] else "",      # Better empty handling
                three_digit_code=row[4].strip() if row[4] else "",  # Better empty handling
                record_type=row[5].strip()         # Added strip()
            )
            
            # Skip events without acronyms
            if not event.acronym:
                continue
                
            self.events[event.event_id] = event
            
            # Organize events by acronym (case sensitive)
            if event.record_type == "Parent Event":
                self.parents_by_acronym[event.acronym].append(event)
            else:  # IEEE Event
                self.children_by_acronym[event.acronym].append(event)
            
            valid_rows.append(row)  # Add valid row to the list
        
        # Print the remaining valid rows
        for valid_row in valid_rows:
            print(valid_row)

    def process_events(self) -> List[Event]:
        """Process events according to the specified rules."""
        valid_events: Set[str] = set()  # Set of valid event IDs
        
        # Process each acronym group
        processed_acronyms = set()  # Added to track processed acronyms
        
        # First, process all acronyms that have children
        for acronym in set(self.children_by_acronym.keys()):
            if acronym in processed_acronyms:
                continue
                
            children = self.children_by_acronym[acronym]
            parents = self.parents_by_acronym.get(acronym, [])
            
            # Skip if no parent or multiple parents for this exact acronym
            if len(parents) != 1:
                continue
                
            parent = parents[0]
            
            # Verify all children have valid three-digit codes
            valid_children = [child for child in children if child.three_digit_code]
            
            # Skip if no valid children
            if not valid_children:
                continue
            
            # Check if all children have the same 3-digit code
            child_codes = {child.three_digit_code for child in valid_children}
            
            if len(child_codes) == 1:
                # All children have the same code
                parent.three_digit_code = next(iter(child_codes))
            else:
                # Children have different codes
                parent.three_digit_code = "???"
            
            # Add valid events to output set
            valid_events.add(parent.event_id)
            valid_events.update(child.event_id for child in valid_children)
            
            processed_acronyms.add(acronym)
        
        # Return sorted list of valid events
        return sorted(
            [event for event_id, event in self.events.items() if event_id in valid_events],
            key=lambda x: (x.acronym, x.event_id)  # Modified sorting
        )
    