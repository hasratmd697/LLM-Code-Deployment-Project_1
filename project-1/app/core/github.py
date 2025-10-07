from github import Github
from github.Repository import Repository
from typing import Dict, Any
import base64
from app.core.config import settings

class GitHubManager:
    def __init__(self):
        self.github = Github(settings.GITHUB_TOKEN)
        self.user = self.github.get_user()

    async def create_and_deploy(self, task_id: str, files: Dict[str, Any]) -> Dict[str, str]:
        """Create a new repository and deploy the generated code to GitHub Pages."""
        # Create repository name from task ID
        repo_name = f"llm-generated-{task_id}"
        
        try:
            # Create new repository
            repo = self.user.create_repo(
                repo_name,
                description="LLM-generated code for task: " + task_id,
                homepage="",
                private=False,
                has_issues=True,
                has_projects=True,
                has_wiki=True,
                auto_init=True
            )

            # Configure GitHub Pages
            await self._configure_pages(repo)
            
            # Create and commit files
            await self._commit_files(repo, files)
            
            # Get the latest commit SHA
            commits = list(repo.get_commits())
            latest_commit_sha = commits[0].sha if commits else None
            
            return {
                "repo_url": repo.html_url,
                "commit_sha": latest_commit_sha,
                "pages_url": f"https://{self.user.login}.github.io/{repo_name}/"
            }
            
        except Exception as e:
            # In a production environment, you'd want to handle specific exceptions
            raise Exception(f"Failed to create and deploy repository: {str(e)}")

    async def _configure_pages(self, repo: Repository):
        """Configure GitHub Pages for the repository."""
        try:
            repo.create_pages_site(
                source={
                    "branch": "main",
                    "path": "/"
                }
            )
        except Exception as e:
            # Pages might already be configured
            pass

    async def _commit_files(self, repo: Repository, files: Dict[str, Any]):
        """Commit files to the repository."""
        for filename, content in files.items():
            try:
                # Convert content to base64
                content_bytes = content.encode('utf-8')
                base64_content = base64.b64encode(content_bytes).decode('utf-8')
                
                # Check if file exists
                try:
                    existing_file = repo.get_contents(filename)
                    # Update existing file
                    repo.update_file(
                        filename,
                        f"Update {filename}",
                        content,
                        existing_file.sha
                    )
                except:
                    # Create new file
                    repo.create_file(
                        filename,
                        f"Add {filename}",
                        content
                    )
            except Exception as e:
                raise Exception(f"Failed to commit file {filename}: {str(e)}")

    async def update_repository(self, repo_url: str, files: Dict[str, Any]) -> Dict[str, str]:
        """Update an existing repository with new files."""
        try:
            # Extract repository name from URL
            repo_name = repo_url.split("/")[-1]
            repo = self.github.get_repo(f"{self.user.login}/{repo_name}")
            
            # Commit updated files
            await self._commit_files(repo, files)
            
            # Get the latest commit SHA
            commits = list(repo.get_commits())
            latest_commit_sha = commits[0].sha if commits else None
            
            return {
                "repo_url": repo.html_url,
                "commit_sha": latest_commit_sha,
                "pages_url": f"https://{self.user.login}.github.io/{repo_name}/"
            }
            
        except Exception as e:
            raise Exception(f"Failed to update repository: {str(e)}")