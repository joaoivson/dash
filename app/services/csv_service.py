import pandas as pd
from typing import List, Dict, Any, Tuple
from datetime import datetime
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

# Colunas obrigatórias esperadas no CSV
REQUIRED_COLUMNS = ["date", "product", "revenue", "cost", "commission"]


class CSVValidationError(Exception):
    """Exception raised for CSV validation errors."""
    pass


class CSVService:
    """Service for processing and validating CSV files."""

    @staticmethod
    def validate_csv(file_content: bytes, filename: str) -> Tuple[pd.DataFrame, List[str]]:
        """
        Validate and parse CSV file.
        
        Args:
            file_content: Raw bytes of the CSV file
            filename: Original filename
            
        Returns:
            Tuple of (DataFrame, list of errors)
        """
        errors = []
        
        try:
            # Try to read CSV with different encodings
            df = None
            for encoding in ['utf-8', 'latin-1', 'iso-8859-1']:
                try:
                    df = pd.read_csv(BytesIO(file_content), encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                errors.append("Não foi possível decodificar o arquivo CSV. Verifique a codificação.")
                return None, errors
            
            # Check if DataFrame is empty
            if df.empty:
                errors.append("O arquivo CSV está vazio.")
                return None, errors
            
            # Normalize column names (lowercase, strip whitespace)
            df.columns = df.columns.str.lower().str.strip()
            
            # Check required columns
            missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
            if missing_columns:
                errors.append(f"Colunas obrigatórias ausentes: {', '.join(missing_columns)}")
                return None, errors
            
            # Select only required columns
            df = df[REQUIRED_COLUMNS].copy()
            
            # Remove rows with all NaN values
            df = df.dropna(how='all')
            
            # Validate and convert date column
            try:
                df['date'] = pd.to_datetime(df['date'], errors='coerce')
            except Exception as e:
                errors.append(f"Erro ao converter coluna 'date': {str(e)}")
                return None, errors
            
            # Check for invalid dates
            invalid_dates = df['date'].isna().sum()
            if invalid_dates > 0:
                errors.append(f"{invalid_dates} linha(s) com data inválida foram removidas.")
                df = df.dropna(subset=['date'])
            
            # Validate numeric columns
            numeric_columns = ['revenue', 'cost', 'commission']
            for col in numeric_columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                except Exception as e:
                    errors.append(f"Erro ao converter coluna '{col}': {str(e)}")
                    return None, errors
            
            # Check for invalid numeric values
            for col in numeric_columns:
                invalid_count = df[col].isna().sum()
                if invalid_count > 0:
                    errors.append(f"{invalid_count} linha(s) com valores inválidos em '{col}' foram removidas.")
                    df = df.dropna(subset=[col])
            
            # Validate product column (should be string)
            df['product'] = df['product'].astype(str).str.strip()
            df = df[df['product'] != '']
            df = df[df['product'] != 'nan']
            
            # Ensure numeric values are non-negative
            for col in numeric_columns:
                negative_count = (df[col] < 0).sum()
                if negative_count > 0:
                    errors.append(f"{negative_count} linha(s) com valores negativos em '{col}' foram corrigidas para 0.")
                    df[col] = df[col].clip(lower=0)
            
            # Calculate profit
            df['profit'] = df['revenue'] - df['cost'] - df['commission']
            
            # Convert date to date only (remove time)
            df['date'] = df['date'].dt.date
            
            # Reset index
            df = df.reset_index(drop=True)
            
            # Final validation - check if DataFrame is still not empty
            if df.empty:
                errors.append("Após validação, nenhuma linha válida restou no arquivo.")
                return None, errors
            
            return df, errors
            
        except pd.errors.EmptyDataError:
            errors.append("O arquivo CSV está vazio ou mal formatado.")
            return None, errors
        except Exception as e:
            logger.error(f"Erro ao processar CSV: {str(e)}")
            errors.append(f"Erro ao processar arquivo CSV: {str(e)}")
            return None, errors

    @staticmethod
    def dataframe_to_dict_list(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Convert DataFrame to list of dictionaries for database insertion.
        
        Args:
            df: Validated DataFrame
            
        Returns:
            List of dictionaries
        """
        return df.to_dict('records')

