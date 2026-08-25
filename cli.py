"""
Command-line interface for Vietnamese Font Converter
"""

import argparse
import sys
import os
from document_converter import DocumentConverter
from vni_unicode_mapping import vni_to_unicode, unicode_to_vni


def main():
    parser = argparse.ArgumentParser(
        description="Vietnamese Font Converter - Convert between VNI and Unicode fonts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert file with auto-detection
  python cli.py input.docx
  
  # Convert file with specific direction
  python cli.py input.docx -t vni_to_unicode
  
  # Convert text directly
  python cli.py -text "VNI encoded text" -t vni_to_unicode
  
  # Convert file and save to specific location
  python cli.py input.xlsx -o output.xlsx -t unicode_to_vni
        """
    )
    
    parser.add_argument('file', nargs='?', help='Input file path (DOCX or XLSX)')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-t', '--type', 
                        choices=['auto', 'vni_to_unicode', 'unicode_to_vni'],
                        default='auto',
                        help='Conversion type (default: auto)')
    parser.add_argument('-text', '--text', help='Text to convert')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Check if text or file conversion
    if args.text:
        # Text conversion
        print("=" * 60)
        print("Vietnamese Font Converter - Text Mode")
        print("=" * 60)
        
        conversion_type = args.type if args.type != 'auto' else 'vni_to_unicode'
        
        if conversion_type == 'vni_to_unicode':
            result = vni_to_unicode(args.text)
            print(f"\nVNI → Unicode conversion:")
            print(f"Input:  {args.text}")
            print(f"Output: {result}")
        else:
            result = unicode_to_vni(args.text)
            print(f"\nUnicode → VNI conversion:")
            print(f"Input:  {args.text}")
            print(f"Output: {result}")
        
        print("=" * 60)
    
    elif args.file:
        # File conversion
        print("=" * 60)
        print("Vietnamese Font Converter - File Mode")
        print("=" * 60)
        
        if not os.path.exists(args.file):
            print(f"❌ Error: File not found - {args.file}")
            sys.exit(1)
        
        converter = DocumentConverter()
        
        # Generate output path if not specified
        output_path = args.output
        if not output_path:
            base, ext = os.path.splitext(args.file)
            output_path = f"{base}_converted{ext}"
        
        print(f"\n📄 Input:  {args.file}")
        print(f"💾 Output: {output_path}")
        print(f"🔄 Type:   {args.type}")
        
        if args.verbose:
            print("\n[Verbose mode enabled]")
        
        print("\n⏳ Converting...")
        
        success, message, output = converter.convert_file(
            args.file, output_path, args.type
        )
        
        if success:
            print(f"✅ Success: {message}")
            print(f"📁 File saved to: {output}")
        else:
            print(f"❌ Error: {message}")
            if args.verbose and converter.errors:
                print("\nDetailed errors:")
                for error in converter.errors:
                    print(f"  - {error}")
            sys.exit(1)
        
        print("=" * 60)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
