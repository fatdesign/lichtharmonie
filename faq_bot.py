import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- KONFIGURATION ------------------------
# Hier deinen neuen Bot-Token einfügen:
BOT_TOKEN = "8295614352:AAGQ-NyPs08aaUqBo20X_D6SyVCLvzn0moQ" 
# ------------------------------------------

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Antworten-Datenbank
FAQ_DATA = {
    "preis": "💰 **Preise & Angebote:**\n- Laserhaarentfernung: ab 49€\n- Theta Healing: 120€ / Sitzung\n- Bioenergie: 100€ / Sitzung\n- Klangtherapie: 80€\n\nSchau dir gerne unsere vollständige Preisliste auf der Webseite an!",
    "termin": "📅 **Terminbuchung:**\nDu kannst Termine direkt über unsere Webseite buchen: https://lichtharmonie.at/#booking\n\nOder ruf uns an unter: +43 650 905 31 21",
    "adresse": "📍 **Standort:**\nDie genaue Adresse in Tirol wird dir bei der Terminbuchung mitgeteilt.",
    "öffnungszeiten": "⏰ **Öffnungszeiten:**\nMo-Fr: 09:00 - 18:00 Uhr\nSa: 10:00 - 14:00 Uhr",
    "kontakt": "📞 **Kontakt:**\nTelefon: +43 650 905 31 21\nEmail: info@lichtharmonie.at",
    
    # THETA HEALING - Ausführliche Informationen
    "theta": """🌟 **THETA HEALING - Umfassende Informationen**

**Was ist Theta Healing?**
Theta Healing ist eine Meditations- und Energieheilungstechnik, die dir hilft, in einen tiefen Entspannungszustand (Theta-Gehirnwellenzustand) zu gelangen. In diesem Zustand können wir gemeinsam limitierende Glaubenssätze, emotionale Blockaden und negative Gedankenmuster identifizieren und transformieren.

**Wer kann Theta Healing anwenden?**
✅ Jeder Mensch, unabhängig von Alter, Hintergrund oder religiöser Überzeugung
✅ Menschen mit emotionalen Belastungen (Stress, Angst, Trauer)
✅ Personen, die persönliches Wachstum anstreben
✅ Menschen mit chronischen Beschwerden (als Ergänzung zur medizinischen Behandlung)
✅ Alle, die ihre Intuition stärken möchten

**Was bewirkt Theta Healing?**
💫 Auflösung emotionaler Blockaden und negativer Glaubenssätze
💫 Stärkung der Intuition und des inneren Bewusstseins
💫 Reduzierung von Stress, Angst und Depression
💫 Förderung von Selbstvertrauen und Selbstwert
💫 Unterstützung bei der Verarbeitung von Traumata
💫 Verbesserung des allgemeinen Wohlbefindens
💫 Hilfe bei der Manifestation persönlicher Ziele

**Langfristige Heilung/Verbesserung?**
Ja! Viele Klienten berichten von tiefgreifenden, langanhaltenden Veränderungen:
• Energetische Verschiebungen wirken bis zu 3 Tage nach der Sitzung
• Positive Veränderungen integrieren sich über mehrere Wochen
• Langfristig: Neues Bewusstsein für Gedankenmuster und deren Einfluss auf das Leben
• Nachhaltige Transformation bei regelmäßiger Anwendung

**Gibt es Risiken?**
⚠️ Theta Healing ist KEIN Ersatz für medizinische Behandlung!
⚠️ Es sollte immer ergänzend zur konventionellen Medizin angewendet werden
⚠️ Bei schweren psychischen Erkrankungen bitte vorher mit deinem Arzt sprechen
✅ Ansonsten gilt: Theta Healing ist eine sanfte, nicht-invasive Methode ohne körperliche Risiken

**Preis:** 120€ pro Sitzung

📅 Termin buchen: https://lichtharmonie.at/#booking""",

    "healing": """🌟 **THETA HEALING - Umfassende Informationen**

**Was ist Theta Healing?**
Theta Healing ist eine Meditations- und Energieheilungstechnik, die dir hilft, in einen tiefen Entspannungszustand (Theta-Gehirnwellenzustand) zu gelangen. In diesem Zustand können wir gemeinsam limitierende Glaubenssätze, emotionale Blockaden und negative Gedankenmuster identifizieren und transformieren.

**Wer kann Theta Healing anwenden?**
✅ Jeder Mensch, unabhängig von Alter, Hintergrund oder religiöser Überzeugung
✅ Menschen mit emotionalen Belastungen (Stress, Angst, Trauer)
✅ Personen, die persönliches Wachstum anstreben
✅ Menschen mit chronischen Beschwerden (als Ergänzung zur medizinischen Behandlung)
✅ Alle, die ihre Intuition stärken möchten

**Was bewirkt Theta Healing?**
💫 Auflösung emotionaler Blockaden und negativer Glaubenssätze
💫 Stärkung der Intuition und des inneren Bewusstseins
💫 Reduzierung von Stress, Angst und Depression
💫 Förderung von Selbstvertrauen und Selbstwert
💫 Unterstützung bei der Verarbeitung von Traumata
💫 Verbesserung des allgemeinen Wohlbefindens
💫 Hilfe bei der Manifestation persönlicher Ziele

**Langfristige Heilung/Verbesserung?**
Ja! Viele Klienten berichten von tiefgreifenden, langanhaltenden Veränderungen:
• Energetische Verschiebungen wirken bis zu 3 Tage nach der Sitzung
• Positive Veränderungen integrieren sich über mehrere Wochen
• Langfristig: Neues Bewusstsein für Gedankenmuster und deren Einfluss auf das Leben
• Nachhaltige Transformation bei regelmäßiger Anwendung

**Gibt es Risiken?**
⚠️ Theta Healing ist KEIN Ersatz für medizinische Behandlung!
⚠️ Es sollte immer ergänzend zur konventionellen Medizin angewendet werden
⚠️ Bei schweren psychischen Erkrankungen bitte vorher mit deinem Arzt sprechen
✅ Ansonsten gilt: Theta Healing ist eine sanfte, nicht-invasive Methode ohne körperliche Risiken

**Preis:** 120€ pro Sitzung

📅 Termin buchen: https://lichtharmonie.at/#booking""",

    "energiearbeit": """🌟 **THETA HEALING - Umfassende Informationen**

**Was ist Theta Healing?**
Theta Healing ist eine Meditations- und Energieheilungstechnik, die dir hilft, in einen tiefen Entspannungszustand (Theta-Gehirnwellenzustand) zu gelangen. In diesem Zustand können wir gemeinsam limitierende Glaubenssätze, emotionale Blockaden und negative Gedankenmuster identifizieren und transformieren.

**Wer kann Theta Healing anwenden?**
✅ Jeder Mensch, unabhängig von Alter, Hintergrund oder religiöser Überzeugung
✅ Menschen mit emotionalen Belastungen (Stress, Angst, Trauer)
✅ Personen, die persönliches Wachstum anstreben
✅ Menschen mit chronischen Beschwerden (als Ergänzung zur medizinischen Behandlung)
✅ Alle, die ihre Intuition stärken möchten

**Was bewirkt Theta Healing?**
💫 Auflösung emotionaler Blockaden und negativer Glaubenssätze
💫 Stärkung der Intuition und des inneren Bewusstseins
💫 Reduzierung von Stress, Angst und Depression
💫 Förderung von Selbstvertrauen und Selbstwert
💫 Unterstützung bei der Verarbeitung von Traumata
💫 Verbesserung des allgemeinen Wohlbefindens
💫 Hilfe bei der Manifestation persönlicher Ziele

**Langfristige Heilung/Verbesserung?**
Ja! Viele Klienten berichten von tiefgreifenden, langanhaltenden Veränderungen:
• Energetische Verschiebungen wirken bis zu 3 Tage nach der Sitzung
• Positive Veränderungen integrieren sich über mehrere Wochen
• Langfristig: Neues Bewusstsein für Gedankenmuster und deren Einfluss auf das Leben
• Nachhaltige Transformation bei regelmäßiger Anwendung

**Gibt es Risiken?**
⚠️ Theta Healing ist KEIN Ersatz für medizinische Behandlung!
⚠️ Es sollte immer ergänzend zur konventionellen Medizin angewendet werden
⚠️ Bei schweren psychischen Erkrankungen bitte vorher mit deinem Arzt sprechen
✅ Ansonsten gilt: Theta Healing ist eine sanfte, nicht-invasive Methode ohne körperliche Risiken

**Preis:** 120€ pro Sitzung

📅 Termin buchen: https://lichtharmonie.at/#booking""",

    # LASERHAARENTFERNUNG - Ausführliche Informationen
    "laser": """✨ **LASERHAARENTFERNUNG - Alle wichtigen Informationen**

**Modernste Diodenlaser-Technologie**
Wir nutzen hochmoderne Diodenlaser für eine schmerzarme, effektive und sichere Haarentfernung - geeignet für alle Hauttypen!

**Vorbereitung vor dem Termin - WICHTIG!**
📋 24-48h vorher: Behandlungsbereich rasieren (NICHT wachsen/epilieren!)
☀️ 2-4 Wochen vorher: Keine Sonnenexposition, kein Solarium, keine Selbstbräuner
🧴 Am Behandlungstag: Keine Cremes, Make-up, Deo oder Lotionen auf der Haut
❌ 4-6 Wochen vorher: Kein Wachsen, Zupfen oder Enthaarungscremes verwenden
💊 Teile uns mit, ob du lichtempfindliche Medikamente nimmst

**Dauer der Sitzungen nach Körperbereich:**
⚡ Kleine Bereiche (Oberlippe, Kinn, Achseln): 5-15 Minuten
⚡ Mittlere Bereiche (Bikinizone, Unterarme, Unterschenkel): 15-30 Minuten
⚡ Große Bereiche (Beine komplett, Rücken, Brust): 30-90 Minuten
⚡ Ganzkörper-Behandlung: über 60 Minuten

**Gibt es Risiken?**
✅ Generell sehr sicher bei professioneller Anwendung!

Mögliche temporäre Nebenwirkungen:
• Leichte Rötung und Schwellung (verschwindet nach wenigen Stunden)
• Selten: Vorübergehende Pigmentveränderungen (meist temporär)
• Sehr selten: Blasenbildung bei falscher Anwendung

⚠️ WICHTIG: Professionelle Behandlung minimiert alle Risiken!

**Nachsorge - Was du beachten solltest:**
❄️ Sofort nach der Behandlung: Kühle Kompressen auflegen
🧴 Aloe Vera Gel oder milde Feuchtigkeitscreme verwenden
☀️ 2 Wochen Sonnenschutz (SPF 30+) und keine direkte Sonne!
🏃‍♀️ 24-72h: Keine Sauna, heißen Bäder, Sport oder Schwitzen
👕 Lockere, atmungsaktive Kleidung tragen
🚫 48h: Keine parfümierten Produkte, Peelings oder Make-up (je nach Bereich)
✋ Nicht kratzen oder die Haut reizen

**Preise:** Ab 49€ (je nach Behandlungsbereich)

📅 Jetzt Termin buchen: https://lichtharmonie.at/#booking""",

    "haarentfernung": """✨ **LASERHAARENTFERNUNG - Alle wichtigen Informationen**

**Modernste Diodenlaser-Technologie**
Wir nutzen hochmoderne Diodenlaser für eine schmerzarme, effektive und sichere Haarentfernung - geeignet für alle Hauttypen!

**Vorbereitung vor dem Termin - WICHTIG!**
📋 24-48h vorher: Behandlungsbereich rasieren (NICHT wachsen/epilieren!)
☀️ 2-4 Wochen vorher: Keine Sonnenexposition, kein Solarium, keine Selbstbräuner
🧴 Am Behandlungstag: Keine Cremes, Make-up, Deo oder Lotionen auf der Haut
❌ 4-6 Wochen vorher: Kein Wachsen, Zupfen oder Enthaarungscremes verwenden
💊 Teile uns mit, ob du lichtempfindliche Medikamente nimmst

**Dauer der Sitzungen nach Körperbereich:**
⚡ Kleine Bereiche (Oberlippe, Kinn, Achseln): 5-15 Minuten
⚡ Mittlere Bereiche (Bikinizone, Unterarme, Unterschenkel): 15-30 Minuten
⚡ Große Bereiche (Beine komplett, Rücken, Brust): 30-90 Minuten
⚡ Ganzkörper-Behandlung: über 60 Minuten

**Gibt es Risiken?**
✅ Generell sehr sicher bei professioneller Anwendung!

Mögliche temporäre Nebenwirkungen:
• Leichte Rötung und Schwellung (verschwindet nach wenigen Stunden)
• Selten: Vorübergehende Pigmentveränderungen (meist temporär)
• Sehr selten: Blasenbildung bei falscher Anwendung

⚠️ WICHTIG: Professionelle Behandlung minimiert alle Risiken!

**Nachsorge - Was du beachten solltest:**
❄️ Sofort nach der Behandlung: Kühle Kompressen auflegen
🧴 Aloe Vera Gel oder milde Feuchtigkeitscreme verwenden
☀️ 2 Wochen Sonnenschutz (SPF 30+) und keine direkte Sonne!
🏃‍♀️ 24-72h: Keine Sauna, heißen Bäder, Sport oder Schwitzen
👕 Lockere, atmungsaktive Kleidung tragen
🚫 48h: Keine parfümierten Produkte, Peelings oder Make-up (je nach Bereich)
✋ Nicht kratzen oder die Haut reizen

**Preise:** Ab 49€ (je nach Behandlungsbereich)

📅 Jetzt Termin buchen: https://lichtharmonie.at/#booking""",

    "vorbereitung": """✨ **LASERHAARENTFERNUNG - Alle wichtigen Informationen**

**Modernste Diodenlaser-Technologie**
Wir nutzen hochmoderne Diodenlaser für eine schmerzarme, effektive und sichere Haarentfernung - geeignet für alle Hauttypen!

**Vorbereitung vor dem Termin - WICHTIG!**
📋 24-48h vorher: Behandlungsbereich rasieren (NICHT wachsen/epilieren!)
☀️ 2-4 Wochen vorher: Keine Sonnenexposition, kein Solarium, keine Selbstbräuner
🧴 Am Behandlungstag: Keine Cremes, Make-up, Deo oder Lotionen auf der Haut
❌ 4-6 Wochen vorher: Kein Wachsen, Zupfen oder Enthaarungscremes verwenden
💊 Teile uns mit, ob du lichtempfindliche Medikamente nimmst

**Dauer der Sitzungen nach Körperbereich:**
⚡ Kleine Bereiche (Oberlippe, Kinn, Achseln): 5-15 Minuten
⚡ Mittlere Bereiche (Bikinizone, Unterarme, Unterschenkel): 15-30 Minuten
⚡ Große Bereiche (Beine komplett, Rücken, Brust): 30-90 Minuten
⚡ Ganzkörper-Behandlung: über 60 Minuten

**Gibt es Risiken?**
✅ Generell sehr sicher bei professioneller Anwendung!

Mögliche temporäre Nebenwirkungen:
• Leichte Rötung und Schwellung (verschwindet nach wenigen Stunden)
• Selten: Vorübergehende Pigmentveränderungen (meist temporär)
• Sehr selten: Blasenbildung bei falscher Anwendung

⚠️ WICHTIG: Professionelle Behandlung minimiert alle Risiken!

**Nachsorge - Was du beachten solltest:**
❄️ Sofort nach der Behandlung: Kühle Kompressen auflegen
🧴 Aloe Vera Gel oder milde Feuchtigkeitscreme verwenden
☀️ 2 Wochen Sonnenschutz (SPF 30+) und keine direkte Sonne!
🏃‍♀️ 24-72h: Keine Sauna, heißen Bäder, Sport oder Schwitzen
👕 Lockere, atmungsaktive Kleidung tragen
🚫 48h: Keine parfümierten Produkte, Peelings oder Make-up (je nach Bereich)
✋ Nicht kratzen oder die Haut reizen

**Preise:** Ab 49€ (je nach Behandlungsbereich)

📅 Jetzt Termin buchen: https://lichtharmonie.at/#booking""",

    "seelenarbeit": "☯ **Seelenarbeit:**\nTheta Healing, Klangtherapie und Energiearbeit helfen dir, Blockaden zu lösen und in deine Mitte zu kommen.\n\nFür detaillierte Infos zu Theta Healing, schreibe einfach 'Theta Healing' oder 'Healing'!",
    
    # BIOENERGIE - Umfassende Informationen
    "bioenergie": """🌿 **BIOENERGIE - Umfassende Informationen**

**Was ist Bioenergie?**
Bioenergie (auch Bioenergetische Analyse genannt) ist ein körperpsychotherapeutisches Verfahren, das von Alexander Lowen entwickelt wurde. Es basiert auf der Erkenntnis, dass Körper und Seele eine Einheit bilden.

🔑 **Kernkonzept:**
Psychische Konflikte und unterdrückte Emotionen manifestieren sich in körperlichen Blockaden und chronischen Muskelverspannungen. Diese "muskuläre Panzerung" beeinträchtigt den freien Fluss der Lebensenergie (Bioenergie) durch den Körper.

**Für wen ist Bioenergie geeignet?**
✅ Angststörungen und Depressionen
✅ Stress und Burnout
✅ Traumata und PTBS
✅ Beziehungsprobleme
✅ Chronische Verspannungen
✅ Psychosomatische Beschwerden
✅ Persönlichkeitsentwicklung

**Wie läuft eine Sitzung ab?**
1️⃣ **Analyse & Beobachtung:** Körperhaltung, Atmung, Energieniveau
2️⃣ **Körperarbeit:** Atemübungen, gezielte Bewegungen, Körperhaltungen
3️⃣ **Analytisches Gespräch:** Verbindung körperlicher Erfahrungen mit persönlicher Geschichte

⏱️ **Dauer:** 50-90 Minuten pro Sitzung

**Was bewirkt Bioenergie?**
✨ Lösung emotionaler Blockaden
✨ Stressabbau und Entspannung
✨ Mehr Lebensenergie und Vitalität
✨ Körperliche Entspannung
✨ Stärkung des Selbstbewusstseins
✨ Mehr Lebendigkeit und Lebensqualität

**Wichtige Hinweise:**
⚠️ Kein Ersatz für medizinische Behandlung
⚠️ Nicht von gesetzlichen Krankenkassen erstattet
⚠️ Wissenschaftliche Wirksamkeit noch nicht vollständig belegt

💰 **Preis:** 100€ pro Sitzung

📅 Termin buchen: https://lichtharmonie.at/#booking
""",
    "bioenergetik": """🌿 **BIOENERGIE - Umfassende Informationen**

**Was ist Bioenergie?**
Bioenergie (auch Bioenergetische Analyse genannt) ist ein körperpsychotherapeutisches Verfahren, das von Alexander Lowen entwickelt wurde. Es basiert auf der Erkenntnis, dass Körper und Seele eine Einheit bilden.

🔑 **Kernkonzept:**
Psychische Konflikte und unterdrückte Emotionen manifestieren sich in körperlichen Blockaden und chronischen Muskelverspannungen. Diese "muskuläre Panzerung" beeinträchtigt den freien Fluss der Lebensenergie (Bioenergie) durch den Körper.

**Für wen ist Bioenergie geeignet?**
✅ Angststörungen und Depressionen
✅ Stress und Burnout
✅ Traumata und PTBS
✅ Beziehungsprobleme
✅ Chronische Verspannungen
✅ Psychosomatische Beschwerden
✅ Persönlichkeitsentwicklung

**Wie läuft eine Sitzung ab?**
1️⃣ **Analyse & Beobachtung:** Körperhaltung, Atmung, Energieniveau
2️⃣ **Körperarbeit:** Atemübungen, gezielte Bewegungen, Körperhaltungen
3️⃣ **Analytisches Gespräch:** Verbindung körperlicher Erfahrungen mit persönlicher Geschichte

⏱️ **Dauer:** 50-90 Minuten pro Sitzung

**Was bewirkt Bioenergie?**
✨ Lösung emotionaler Blockaden
✨ Stressabbau und Entspannung
✨ Mehr Lebensenergie und Vitalität
✨ Körperliche Entspannung
✨ Stärkung des Selbstbewusstseins
✨ Mehr Lebendigkeit und Lebensqualität

**Wichtige Hinweise:**
⚠️ Kein Ersatz für medizinische Behandlung
⚠️ Nicht von gesetzlichen Krankenkassen erstattet
⚠️ Wissenschaftliche Wirksamkeit noch nicht vollständig belegt

💰 **Preis:** 100€ pro Sitzung

📅 Termin buchen: https://lichtharmonie.at/#booking
""",
    "körperarbeit": "🌿 **Bioenergie - Körperarbeit**\n\nBioenergie nutzt Körperarbeit zur Lösung emotionaler Blockaden. Durch Atemübungen, gezielte Bewegungen und Körperhaltungen wird die Lebensenergie wieder zum Fließen gebracht.\n\n💰 Preis: 100€ / Sitzung\n📅 Termin: https://lichtharmonie.at/#booking",
    "blockaden": "🌿 **Bioenergie - Blockaden lösen**\n\nBioenergie hilft dabei, emotionale und körperliche Blockaden zu lösen. Unterdrückte Emotionen manifestieren sich oft als muskuläre Verspannungen. Durch Körperarbeit und Atemübungen werden diese Blockaden gelöst.\n\n💰 Preis: 100€ / Sitzung\n📅 Termin: https://lichtharmonie.at/#booking",
    "verspannungen": "🌿 **Bioenergie bei Verspannungen**\n\nChronische Verspannungen sind oft Ausdruck unterdrückter Emotionen. Bioenergie kombiniert Körperarbeit mit psychologischer Analyse, um diese muskulären Blockaden zu lösen und den Energiefluss wiederherzustellen.\n\n💰 Preis: 100€ / Sitzung\n📅 Termin: https://lichtharmonie.at/#booking",
}

# Tasten-Layout für das Menü
MENU_BUTTONS = [
    ["💰 Preise", "📅 Termin Buchen"],
    ["📍 Adresse", "⏰ Öffnungszeiten"],
    ["✨ Laser Info", "🌿 Bioenergie"],
    ["🌟 Theta Healing", "📞 Kontakt"]
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "✨ **Willkommen bei LICHTHARMONIE by Aksu!** ✨\n\n"
        "Ich bin dein virtueller Assistent. Wähle einfach ein Thema unten aus dem Menü:",
        reply_markup=ReplyKeyboardMarkup(MENU_BUTTONS, resize_keyboard=True)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text.lower()
    
    # Intelligente Suche nach Stichworten
    found_answer = False
    for keyword, answer in FAQ_DATA.items():
        if keyword in user_text:
            await update.message.reply_text(
                answer,
                reply_markup=ReplyKeyboardMarkup(MENU_BUTTONS, resize_keyboard=True)
            )
            found_answer = True
            break
    
    # Fallback, wenn nichts gefunden wurde
    if not found_answer:
        await update.message.reply_text(
            f"Das habe ich leider nicht verstanden. 🤔\n"
            f"Bitte wähle einen der Punkte aus dem Menü unten 👇",
            reply_markup=ReplyKeyboardMarkup(MENU_BUTTONS, resize_keyboard=True)
        )

if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT, handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    print("🤖 Bot ist gestartet und wartet auf Nachrichten...")
    application.run_polling()
