/*

Advanced Access Control

    A modified access control that will work with Black Dragon shell terminal to
    give access, determine access, etc.

 */

/*

AddUser(user, password)

Adds a user to the system

*/

#include <iostream>
#include <string>
#include <queue>
#include <sys/stat.h>
#include <filesystem>
#include <dirent.h>

using namespace std;

using recursive_directory_iterator = std::filesystem::recursive_directory_iterator;

bool PathExists(std::string path)
{
    struct stat buffer;
    return (stat(path.c_str(), &buffer) == 0);
}

queue<std::string> ImportUsers(std::string path)
{

    // the list to return at the end
    queue<std::string> users;

    for (const auto &dirEntry : recursive_directory_iterator(path))
        std::cout << dirEntry << std::endl;

    return users;
}

int AddUser(std::string user, std::string password)
{
    // check if user name isn't blank
    if (user.compare("") == 0)
    {
        cout << "Error: Username is missing"
             << "\n";
        return -1;
    }

    // create users directory if it wasn't created already

    // if the users directory doesn't exist then create it
    if (PathExists("Users") == 0)
    {
        int status = mkdir("Users", S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
        if (status == 0)
        {
            cout << "USERS DIRECTORY CREATED\n";
        }
    }

    // import the users list from what exists
    queue<std::string> userList = ImportUsers("Users");

    return 0;
}

int main()
{
    AddUser("username", "password");
    return 0;
}