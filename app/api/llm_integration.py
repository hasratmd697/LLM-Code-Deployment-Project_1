from app.core.llm import LLMCodeGenerator
from app.core.github import GitHubManager
from app.api.endpoints import CodeRequest, EvaluationResponse

# Initialize components
llm_generator = LLMCodeGenerator()
github_manager = GitHubManager()

async def process_initial_request(request: CodeRequest) -> EvaluationResponse:
    # Generate code using LLM
    code_files = await llm_generator.generate_code(request.brief, request.checks)
    
    # Deploy to GitHub Pages
    repo_info = await github_manager.create_and_deploy(request.task, code_files)
    
    return EvaluationResponse(
        email=request.email,
        task=request.task,
        round=request.round,
        nonce=request.nonce,
        **repo_info
    )

async def process_revision_request(request: CodeRequest) -> EvaluationResponse:
    # Generate updated code using LLM
    updated_files = await llm_generator.generate_code(
        f"REVISION REQUEST - Previous repository exists. {request.brief}",
        request.checks
    )
    
    # Find the repository URL from round 1
    # In a production environment, you'd want to store and retrieve this from a database
    repo_url = f"https://github.com/{github_manager.user.login}/llm-generated-{request.task}"
    
    # Update existing repository
    repo_info = await github_manager.update_repository(repo_url, updated_files)
    
    return EvaluationResponse(
        email=request.email,
        task=request.task,
        round=request.round,
        nonce=request.nonce,
        **repo_info
    )