from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import tempfile
import time
import os
from pathlib import Path

app = FastAPI()

class CodeInput(BaseModel):
    code: str
    timeout: int = 5  # Timeout padrão de 5 segundos

@app.post("/execute")
async def execute_code(payload: CodeInput):
    """Executa código Python com segurança e retorna o resultado"""
    try:
        # Cria arquivo temporário em diretório seguro
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            dir=Path("/tmp"),
            delete=False
        ) as tmp:
            tmp.write(payload.code)
            tmp_path = tmp.name

        # Configura ambiente seguro
        env = os.environ.copy()
        env["PYTHONSAFEPATH"] = "1"
        
        start_time = time.time()
        result = subprocess.run(
            ["python", tmp_path],
            capture_output=True,
            text=True,
            timeout=payload.timeout,
            env=env
        )
        exec_time = time.time() - start_time

        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exec_time": round(exec_time, 3),
            "exit_code": result.returncode
        }

    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=408,
            detail=f"Execution timed out after {payload.timeout} seconds"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Execution error: {str(e)}"
        )
    finally:
        # Garante a remoção do arquivo temporário
        if 'tmp_path' in locals() and os.path.exists(tmp_path):
            os.unlink(tmp_path)