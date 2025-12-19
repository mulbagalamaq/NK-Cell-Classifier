#!/usr/bin/env python3
"""
Download GEO data for NK cell multimodal analysis.

Data sources:
- GSE264696: CITE-seq (primary analysis dataset)
- GSE264693: ATAC-seq (chromatin accessibility)
"""

import os
import subprocess
from pathlib import Path
from typing import List
import requests
from tqdm import tqdm


def download_file(url: str, output_path: Path, chunk_size: int = 8192) -> bool:
    """
    Download a file with progress bar.
    
    Parameters
    ----------
    url : str
        URL to download
    output_path : Path
        Local path to save file
    chunk_size : int
        Download chunk size in bytes
        
    Returns
    -------
    bool
        True if successful, False otherwise
    """
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(output_path, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, 
                      desc=output_path.name, ncols=80) as pbar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    pbar.update(len(chunk))
        return True
    except Exception as e:
        print(f"  Error: {e}")
        return False


def main():
    """Main download routine."""
    
    project_root = Path(__file__).parent.parent
    raw_dir = project_root / 'data' / 'raw'
    
    # CITE-seq data (GSE264696)
    print("\n" + "="*60)
    print("Downloading CITE-seq data (GSE264696)")
    print("="*60)
    
    cite_dir = raw_dir / 'cite_seq'
    cite_dir.mkdir(parents=True, exist_ok=True)
    
    geo_base = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE264nnn/GSE264696/suppl/"
    
    # Main supplementary files
    cite_files = [
        "GSE264696_730_HTO_GEXbarcodes.tsv.gz",
        "GSE264696_730_HTO_GEXfeatures.tsv.gz",
        "GSE264696_730_HTO_GEXmatrix.mtx.gz",
        "GSE264696_3228_HTO_GEXbarcodes.tsv.gz",
        "GSE264696_3228_HTO_GEXfeatures.tsv.gz",
        "GSE264696_3228_HTO_GEXmatrix.mtx.gz",
    ]
    
    for filename in cite_files:
        output_path = cite_dir / filename
        if output_path.exists():
            print(f"Already exists: {filename}")
            continue
        
        url = geo_base + filename
        print(f"Downloading: {filename}")
        download_file(url, output_path)
    
    # ADT (protein) data from GSM samples
    print("\n" + "="*60)
    print("Downloading ADT (protein) data")
    print("="*60)
    
    gsm_samples = {
        "GSM8226272": "730_ADT",
        "GSM8226274": "3228_ADT",
    }
    
    for gsm_id, sample_name in gsm_samples.items():
        for suffix in ['barcodes.tsv.gz', 'features.tsv.gz', 'matrix.mtx.gz']:
            filename = f"{gsm_id}_{sample_name}{suffix}"
            output_path = cite_dir / filename
            
            if output_path.exists():
                print(f"Already exists: {filename}")
                continue
            
            url = f"https://ftp.ncbi.nlm.nih.gov/geo/samples/{gsm_id[:7]}nnn/{gsm_id}/suppl/{filename}"
            print(f"Downloading: {filename}")
            download_file(url, output_path)
    
    # Summary
    print("\n" + "="*60)
    print("Download Summary")
    print("="*60)
    
    files = list(cite_dir.glob('*'))
    print(f"\nCITE-seq directory: {len(files)} files")
    total_size = sum(f.stat().st_size for f in files) / (1024**2)
    print(f"Total size: {total_size:.1f} MB")
    
    for f in sorted(files):
        size_mb = f.stat().st_size / (1024**2)
        print(f"  {f.name}: {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
