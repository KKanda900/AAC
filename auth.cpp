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

int main()
{
    AddUser("username", "password");
    return 0;
}