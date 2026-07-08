"""CAD availability checker - gracefully handles missing dependencies."""


def is_cad_available():
    """Check if CAD dependencies are available."""
    try:
        import pythoncom
        from pyautocad import Autocad
        return True
    except ImportError:
        return False


def get_cad_status():
    """Get detailed CAD status with helpful message."""
    try:
        import pythoncom
        import pyautocad
        return {
            "available": True,
            "message": "AutoCAD drawing support available",
        }
    except ImportError as e:
        return {
            "available": False,
            "message": f"AutoCAD drawing disabled. To enable: pip install -r requirements-optional.txt",
            "error": str(e),
        }
