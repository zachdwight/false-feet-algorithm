#include "poirot_solver.h"

// ============================================================================
// MYSTERY SETUP: The Case of the Vanished Necklace
// ============================================================================

MysteryScenario setup_mystery() {
    MysteryScenario mystery;
    mystery.title = "The Vanished Necklace";
    mystery.victim = "Lady Pembroke";
    mystery.crime = "Theft of the priceless Maharaja Diamond Necklace";
    
    // ===== SUSPECTS =====
    mystery.suspects = {
        Suspect{"butler", "James the Butler", 
                "Years of low wages, bitter resentment",
                "Had access to all rooms at night"},
        
        Suspect{"nephew", "Charles the Nephew",
                "Gambling debts, needs money desperately",
                "Staying at the mansion for the weekend"},
        
        Suspect{"maid", "Margaret the Chambermaid",
                "Romantic rejection by the butler, revenge motive",
                "Cleans the bedroom daily, knows exact location"},
        
        Suspect{"driver", "Robert the Driver",
                "Previous theft conviction, known criminal",
                "Brings guests to and from the house"}
    };
    
    // Set initial suspicion levels (before any evidence)
    mystery.suspects[0].suspicion_level = 45;
    mystery.suspects[1].suspicion_level = 35;
    mystery.suspects[2].suspicion_level = 25;
    mystery.suspects[3].suspicion_level = 60;  // Driver has prior record
    
    // ===== EVIDENCE =====
    
    // Evidence 1: Fingerprints on case
    mystery.all_evidence.push_back(Evidence{
        "evidence_1",
        "Fingerprints on jewelry case",
        "Fresh fingerprints match butler's records",
        {"butler"},  // incriminates butler
        {"maid"},    // exonerates maid
        5            // High priority
    });
    
    // Evidence 2: Witness saw butler in garden
    mystery.all_evidence.push_back(Evidence{
        "evidence_2",
        "Witness: butler in garden at midnight",
        "Kitchen maid saw butler leaving through garden door",
        {"butler"},
        {},
        4
    });
    
    // Evidence 3: Nephew's debts
    mystery.all_evidence.push_back(Evidence{
        "evidence_3",
        "Nephew's gambling debts",
        "Found IOUs totaling 10,000 pounds in nephew's room",
        {"nephew"},
        {},
        4
    });
    
    // Evidence 4: Security footage
    mystery.all_evidence.push_back(Evidence{
        "evidence_4",
        "Security guard reports",
        "No one left the house between 11 PM and 7 AM",
        {},
        {"driver"},  // exonerates driver (wasn't there)
        5
    });
    
    // Evidence 5: Missing jewelry box key
    mystery.all_evidence.push_back(Evidence{
        "evidence_5",
        "Jewelry box key missing",
        "Only butler and Lady Pembroke had keys",
        {"butler"},
        {"nephew", "driver"},
        3
    });
    
    // Evidence 6: Maid's romance with butler
    mystery.all_evidence.push_back(Evidence{
        "evidence_6",
        "Butler rejected maid's romantic advances",
        "Maid was upset about butler's rejection last week",
        {"maid"},
        {},
        3
    });
    
    // Evidence 7: Butler's savings account
    mystery.all_evidence.push_back(Evidence{
        "evidence_7",
        "Butler recently increased savings",
        "Large deposits appeared in butler's account this week",
        {"butler"},
        {},
        5
    });
    
    // Evidence 8: Maid's employment record
    mystery.all_evidence.push_back(Evidence{
        "evidence_8",
        "Maid employed for 15 years, spotless record",
        "No previous theft accusations or suspicions",
        {},
        {"maid"},  // exonerates maid
        4
    });
    
    // Evidence 9: Driver's past conviction
    mystery.all_evidence.push_back(Evidence{
        "evidence_9",
        "Driver's theft conviction from 5 years ago",
        "Served 2 years for jewelry theft",
        {"driver"},
        {},
        5
    });
    
    // Evidence 10: Nephew's hotel stay
    mystery.all_evidence.push_back(Evidence{
        "evidence_10",
        "Nephew seen at local hotel before the theft",
        "Hotel staff confirm nephew was there with 'accomplice'",
        {"nephew"},
        {},
        4
    });
    
    // Evidence 11: The killer piece - Butler's confession note (hidden)
    mystery.all_evidence.push_back(Evidence{
        "evidence_11",
        "Handwriting analysis on butler's personal letters",
        "Matches handwriting on anonymous ransom note found in kitchen",
        {"butler"},
        {},
        5
    });
    
    // Evidence 12: Maid's alibi
    mystery.all_evidence.push_back(Evidence{
        "evidence_12",
        "Maid's sister confirms alibi",
        "Maid was visiting her ill sister until midnight on the night of theft",
        {},
        {"maid"},
        4
    });
    
    // Evidence 13: Driver's vehicle logs
    mystery.all_evidence.push_back(Evidence{
        "evidence_13",
        "Vehicle logs show driver away from house",
        "Driver was in the village all evening, confirmed by pub owner",
        {},
        {"driver"},
        5
    });
    
    return mystery;
}

// ============================================================================
// MAIN: Run the Investigation
// ============================================================================

int main() {
    try {
        std::cout << "\n╔═══════════════════════════════════════════════════════════════════╗\n";
        std::cout << "║                                                                   ║\n";
        std::cout << "║         THE POIROT MYSTERY SOLVER v1.0                            ║\n";
        std::cout << "║    Using Amoeba Algorithm for Investigative Reasoning             ║\n";
        std::cout << "║                                                                   ║\n";
        std::cout << "╚═══════════════════════════════════════════════════════════════════╝\n";
        
        MysteryScenario mystery = setup_mystery();
        MysteryInvestigation investigation(mystery);
        
        investigation.solve();
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << "\n";
        return 1;
    }
    
    return 0;
}
