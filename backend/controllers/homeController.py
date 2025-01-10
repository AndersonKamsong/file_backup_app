from backend.controllers.githubController import GitHubController  
from backend.models.Branch import Branch  

file_backup_token = "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"
controller = GitHubController(file_backup_token)
# file_path = "/home/anderson/Desktop/python/file_backup_app/views"
# print(controller.upload_file(user_found[0][1], "/home/anderson/Desktop/python/file_backup_app/backend/mirgations/backupdb.sql"))
# print(controller.add_folder_to_branch(user_found[0][1],file_path,"views"))

def create_branch_from_folder(user,folder_path):
    try:
        result = controller.create_branch(user[0][1],folder_path)
        branch_found = Branch().findByUserAndName(user_id=user[0][0],branch_name=result['branch_name'])
        print(result)
        if branch_found:
            return {"error": "Branch already exists"}
        new_branch = Branch(
            user_id=user[0][0],
            branch_name=result['branch_name'],
            folder_path=folder_path,
        )
        new_branch.save()
        return {'message':'branch created successful','branch_name':new_branch.branch_name}
    except Exception as e:
        return {"error": str(e)}
    
def backup_to_branch(user,branch_name):
    try:
        branch_found = Branch().findByUserAndName(user_id=user[0][0],branch_name=branch_name)
        print(branch_found)
        if not branch_found:
            return {"error": "Branch donot exists"}
        
        result = controller.add_folder_to_branch(user[0][1],branch_found[0][3],branch_name)
        return {'message':'branch updated successful'}
    except Exception as e:
        return {"error": str(e)}
    
    