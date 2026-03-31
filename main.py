"""
Main Entry Point -- Interactive CLI
Allows users to ask questions and get RAG-powered answers.
"""

from backend.rag_pipeline import RAGPipeline


def main():
    """Run the interactive RAG question-answering interface."""
    
    print("\n" + "=" * 60)
    print("  RAG System -- Stock Market & Investment Analysis")
    print("  Powered by Groq + FAISS + LangChain")
    print("=" * 60)
    
    # Initialize the pipeline
    pipeline = RAGPipeline()
    pipeline.initialize()
    
    print("\n   Type your question below. Type 'quit' or 'exit' to stop.\n")
    
    while True:
        try:
            # Get user input
            question = input("\n>> Your Question: ").strip()
            
            # Check for exit commands
            if question.lower() in ("quit", "exit", "q"):
                print("\n   Goodbye! Thank you for using the RAG system.\n")
                break
            
            # Skip empty input
            if not question:
                print("   Please enter a question.")
                continue
            
            # Process the query
            print("-" * 60)
            result = pipeline.query(question)
            
            # Print the answer
            print("=" * 60)
            print("ANSWER:")
            print("=" * 60)
            print(result["answer"])
            print("=" * 60)
        
        except KeyboardInterrupt:
            print("\n\n   Interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"\n   Error: {e}")
            print("Please try again with a different question.\n")


if __name__ == "__main__":
    main()
