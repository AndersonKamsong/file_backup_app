from backend.controllers.githubController import GitHubController  
from backend.models.Branch import Branch  

# file_backup_token = "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"

controller = GitHubController(file_backup_token)
# file_path = "/home/anderson/Desktop/python/file_backup_app/views"
# print(controller.upload_file(user_found[0][1], "/home/anderson/Desktop/python/file_backup_app/backend/mirgations/backupdb.sql"))
# print(controller.add_folder_to_branch(user_found[0][1],file_path,"views"))

def create_branch_from_folder(user,folder_path):
    try:
        result = controller.create_branch(user[0][1],folder_path)
        if "error" in result:
            return result
        else:
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
        if "error" in result:
            return result
        else:
            return {'message':'branch updated successful'}
    except Exception as e:
        return {"error": str(e)}

def delete_branch(user,branch_name):
    try:
        branch_found = Branch().findByUserAndName(user_id=user[0][0],branch_name=branch_name)
        print(branch_found)
        if not branch_found:
            return {"error": "Branch donot exists"}
        
        result = controller.delete_branch(user[0][1],branch_name)
        if "error" in result:
            return result
        else:
            Branch().delete(branch_id=branch_found[0][0])
            return {'message':'branch updated successful'}
    except Exception as e:
        return {"error": str(e)}

def restore_branch(user,branch_name,folder_path):
    try:
        branch_found = Branch().findByUserAndName(user_id=user[0][0],branch_name=branch_name)
        print(branch_found)
        if not branch_found:
            return {"error": "Branch donot exists"}
        # print("here anderson")
        # print(user)
        result = controller.download_branch(user[0][1],branch_name,folder_path)
        if "error" in result:
            return result
        else:
            return result
    except Exception as e:
        return {"error": str(e)}
    
def get_user_branch(user_id):
    try:
        branch_found = Branch().findByUser(user_id=user_id)
        return {'branch_found':branch_found}
    except Exception as e:
        return {"error": str(e)}