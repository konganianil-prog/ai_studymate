import os
import uuid
from pathlib import Path

class ImageService:
    @staticmethod
    def generate_educational_svg(topic: str, output_dir: str) -> str:
        """
        Generates a clean, educational SVG diagram representing the topic's workflow
        and saves it in output_dir. Returns the relative web URL.
        """
        os.makedirs(output_dir, exist_ok=True)
        filename = f"diagram_{uuid.uuid4().hex[:10]}.svg"
        filepath = os.path.join(output_dir, filename)

        topic_clean = topic.strip()
        topic_lower = topic_clean.lower()

        # Generate custom SVG diagram based on topic domain
        if any(w in topic_lower for w in ['blockchain', 'block', 'crypto', 'ledger']):
            svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 350" width="100%" height="100%">
  <defs>
    <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#6C63FF;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#3B82F6;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#00C9A7;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#10B981;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="#131930" rx="16"/>
  <text x="400" y="45" font-family="Outfit, sans-serif" font-size="20" font-weight="bold" fill="#FFFFFF" text-anchor="middle">BLOCKCHAIN CRYPTOGRAPHIC CHAIN ARCHITECTURE</text>
  
  <!-- Block 0: Genesis -->
  <g transform="translate(60, 90)">
    <rect width="180" height="190" rx="12" fill="#1B2340" stroke="#6C63FF" stroke-width="2"/>
    <rect width="180" height="35" rx="12" fill="url(#grad1)"/>
    <text x="90" y="24" fill="#FFFFFF" font-family="sans-serif" font-weight="bold" font-size="14" text-anchor="middle">Block #0 (Genesis)</text>
    <text x="15" y="65" fill="#94A3B8" font-size="11" font-family="monospace">Prev Hash: 0000000000</text>
    <text x="15" y="95" fill="#00C9A7" font-size="11" font-family="monospace">Data: Tx 1..N</text>
    <text x="15" y="125" fill="#94A3B8" font-size="11" font-family="monospace">Nonce: 184592</text>
    <text x="15" y="155" fill="#FFB800" font-size="11" font-family="monospace">Hash: 0000a4b7e9...</text>
  </g>

  <!-- Arrow 1 -->
  <line x1="240" y1="185" x2="300" y2="185" stroke="#00C9A7" stroke-width="3" stroke-dasharray="5,5"/>
  <polygon points="305,185 295,178 295,192" fill="#00C9A7"/>

  <!-- Block 1 -->
  <g transform="translate(310, 90)">
    <rect width="180" height="190" rx="12" fill="#1B2340" stroke="#00C9A7" stroke-width="2"/>
    <rect width="180" height="35" rx="12" fill="url(#grad2)"/>
    <text x="90" y="24" fill="#0F172A" font-family="sans-serif" font-weight="bold" font-size="14" text-anchor="middle">Block #1</text>
    <text x="15" y="65" fill="#FFB800" font-size="11" font-family="monospace">Prev: 0000a4b7e9...</text>
    <text x="15" y="95" fill="#00C9A7" font-size="11" font-family="monospace">Merkle Root: 7f3b...</text>
    <text x="15" y="125" fill="#94A3B8" font-size="11" font-family="monospace">Nonce: 94821</text>
    <text x="15" y="155" fill="#6C63FF" font-size="11" font-family="monospace">Hash: 0000c82f11...</text>
  </g>

  <!-- Arrow 2 -->
  <line x1="490" y1="185" x2="550" y2="185" stroke="#6C63FF" stroke-width="3" stroke-dasharray="5,5"/>
  <polygon points="555,185 545,178 545,192" fill="#6C63FF"/>

  <!-- Block 2 -->
  <g transform="translate(560, 90)">
    <rect width="180" height="190" rx="12" fill="#1B2340" stroke="#6C63FF" stroke-width="2"/>
    <rect width="180" height="35" rx="12" fill="url(#grad1)"/>
    <text x="90" y="24" fill="#FFFFFF" font-family="sans-serif" font-weight="bold" font-size="14" text-anchor="middle">Block #2</text>
    <text x="15" y="65" fill="#6C63FF" font-size="11" font-family="monospace">Prev: 0000c82f11...</text>
    <text x="15" y="95" fill="#00C9A7" font-size="11" font-family="monospace">Data: Smart Contract</text>
    <text x="15" y="125" fill="#94A3B8" font-size="11" font-family="monospace">Nonce: 44210</text>
    <text x="15" y="155" fill="#FFB800" font-size="11" font-family="monospace">Hash: 000099f0e1...</text>
  </g>
  <text x="400" y="315" font-family="Outfit, sans-serif" font-size="12" fill="#94A3B8" text-anchor="middle">Immutable cryptographic hashes guarantee tamper-proof ledger validation.</text>
</svg>"""
        elif any(w in topic_lower for w in ['neural', 'deep learning', 'cnn', 'ai', 'machine learning']):
            svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 350" width="100%" height="100%">
  <rect width="100%" height="100%" fill="#131930" rx="16"/>
  <text x="400" y="45" font-family="Outfit, sans-serif" font-size="20" font-weight="bold" fill="#FFFFFF" text-anchor="middle">DEEP NEURAL NETWORK ARCHITECTURE</text>
  
  <!-- Input Layer -->
  <g transform="translate(100, 90)">
    <text x="30" y="0" fill="#6C63FF" font-weight="bold" font-size="14" text-anchor="middle">Input Layer</text>
    <circle cx="30" cy="40" r="18" fill="#1B2340" stroke="#6C63FF" stroke-width="3"/>
    <circle cx="30" cy="90" r="18" fill="#1B2340" stroke="#6C63FF" stroke-width="3"/>
    <circle cx="30" cy="140" r="18" fill="#1B2340" stroke="#6C63FF" stroke-width="3"/>
    <circle cx="30" cy="190" r="18" fill="#1B2340" stroke="#6C63FF" stroke-width="3"/>
  </g>

  <!-- Hidden Layer 1 -->
  <g transform="translate(300, 70)">
    <text x="30" y="0" fill="#00C9A7" font-weight="bold" font-size="14" text-anchor="middle">Hidden Layer 1</text>
    <circle cx="30" cy="30" r="18" fill="#1B2340" stroke="#00C9A7" stroke-width="3"/>
    <circle cx="30" cy="75" r="18" fill="#1B2340" stroke="#00C9A7" stroke-width="3"/>
    <circle cx="30" cy="120" r="18" fill="#1B2340" stroke="#00C9A7" stroke-width="3"/>
    <circle cx="30" cy="165" r="18" fill="#1B2340" stroke="#00C9A7" stroke-width="3"/>
    <circle cx="30" cy="210" r="18" fill="#1B2340" stroke="#00C9A7" stroke-width="3"/>
  </g>

  <!-- Hidden Layer 2 -->
  <g transform="translate(500, 70)">
    <text x="30" y="0" fill="#FFB800" font-weight="bold" font-size="14" text-anchor="middle">Hidden Layer 2</text>
    <circle cx="30" cy="45" r="18" fill="#1B2340" stroke="#FFB800" stroke-width="3"/>
    <circle cx="30" cy="105" r="18" fill="#1B2340" stroke="#FFB800" stroke-width="3"/>
    <circle cx="30" cy="165" r="18" fill="#1B2340" stroke="#FFB800" stroke-width="3"/>
  </g>

  <!-- Output Layer -->
  <g transform="translate(680, 100)">
    <text x="30" y="0" fill="#FF6584" font-weight="bold" font-size="14" text-anchor="middle">Output Layer</text>
    <circle cx="30" cy="50" r="18" fill="#1B2340" stroke="#FF6584" stroke-width="3"/>
    <circle cx="30" cy="120" r="18" fill="#1B2340" stroke="#FF6584" stroke-width="3"/>
  </g>

  <text x="400" y="320" font-family="Outfit, sans-serif" font-size="12" fill="#94A3B8" text-anchor="middle">Forward propagation calculates activations; Backpropagation updates weights via gradient descent.</text>
</svg>"""
        else:
            # Generic clean educational process architecture
            svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 350" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#6C63FF;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#00C9A7;stop-opacity:0.8" />
    </linearGradient>
  </defs>
  <rect width="100%" height="100%" fill="#131930" rx="16"/>
  <text x="400" y="45" font-family="Outfit, sans-serif" font-size="20" font-weight="bold" fill="#FFFFFF" text-anchor="middle">{topic_clean.upper()} — SYSTEM ARCHITECTURE</text>
  
  <!-- Step 1 -->
  <g transform="translate(60, 100)">
    <rect width="180" height="150" rx="12" fill="#1B2340" stroke="#6C63FF" stroke-width="2"/>
    <rect width="180" height="30" rx="12" fill="#6C63FF"/>
    <text x="90" y="20" fill="#FFFFFF" font-family="sans-serif" font-weight="bold" font-size="13" text-anchor="middle">1. Input Stage</text>
    <text x="90" y="75" fill="#94A3B8" font-size="12" font-family="sans-serif" text-anchor="middle">Data Ingestion</text>
    <text x="90" y="100" fill="#00C9A7" font-size="11" font-family="sans-serif" text-anchor="middle">Validation &amp; Parsing</text>
  </g>

  <line x1="240" y1="175" x2="300" y2="175" stroke="#6C63FF" stroke-width="3"/>
  <polygon points="305,175 295,168 295,182" fill="#6C63FF"/>

  <!-- Step 2 -->
  <g transform="translate(310, 100)">
    <rect width="180" height="150" rx="12" fill="#1B2340" stroke="#00C9A7" stroke-width="2"/>
    <rect width="180" height="30" rx="12" fill="#00C9A7"/>
    <text x="90" y="20" fill="#0F172A" font-family="sans-serif" font-weight="bold" font-size="13" text-anchor="middle">2. Core Processing</text>
    <text x="90" y="75" fill="#94A3B8" font-size="12" font-family="sans-serif" text-anchor="middle">{topic_clean[:22]}</text>
    <text x="90" y="100" fill="#FFB800" font-size="11" font-family="sans-serif" text-anchor="middle">Optimization &amp; Logic</text>
  </g>

  <line x1="490" y1="175" x2="550" y2="175" stroke="#00C9A7" stroke-width="3"/>
  <polygon points="555,175 545,168 545,182" fill="#00C9A7"/>

  <!-- Step 3 -->
  <g transform="translate(560, 100)">
    <rect width="180" height="150" rx="12" fill="#1B2340" stroke="#FF6584" stroke-width="2"/>
    <rect width="180" height="30" rx="12" fill="#FF6584"/>
    <text x="90" y="20" fill="#FFFFFF" font-family="sans-serif" font-weight="bold" font-size="13" text-anchor="middle">3. Output / Store</text>
    <text x="90" y="75" fill="#94A3B8" font-size="12" font-family="sans-serif" text-anchor="middle">Result Synthesis</text>
    <text x="90" y="100" fill="#10B981" font-size="11" font-family="sans-serif" text-anchor="middle">State Commitment</text>
  </g>

  <text x="400" y="305" font-family="Outfit, sans-serif" font-size="12" fill="#94A3B8" text-anchor="middle">Educational Workflow diagram generated for {topic_clean}</text>
</svg>"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(svg_content)

        return f"/generated/{filename}"
