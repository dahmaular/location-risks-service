import uvicorn


def main():
    """Main function to run the FastAPI server."""
    print("Starting Location Risk Assessment API server...")
    print("API Documentation will be available at: http://localhost:8000/docs")
    print("API will be accessible at: http://localhost:8000")

    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


if __name__ == "__main__":
    main()
