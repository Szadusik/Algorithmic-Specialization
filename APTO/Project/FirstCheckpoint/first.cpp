#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <queue>
#include <bits/stdc++.h>

using namespace std;

struct drone{
    char name;
    pair<int, int> start;
    pair<int, int> end;
};

struct field{
    int distance;
    pair<int,int> precursor;
};

vector<pair<int, int> > checkFields(char* grid[],pair<int,int> field, int n, int m){
    vector<pair<int,int> > moves;
    if(field.first -1 >= 0 && grid[field.first-1][field.second] != '#' && grid[field.first-1][field.second] != '@')
        moves.emplace_back(field.first-1,field.second);

    if(field.first +1 < n && grid[field.first+1][field.second] != '#' && grid[field.first+1][field.second] != '@')
        moves.emplace_back(field.first+1,field.second);

    if(field.second -1 >= 0 && grid[field.first][field.second-1] != '#' && grid[field.first][field.second-1] != '@')
        moves.emplace_back(field.first,field.second-1);

    if(field.second +1 < m && grid[field.first][field.second+1] != '#' && grid[field.first][field.second+1] != '@')
        moves.emplace_back(field.first,field.second+1);

    return moves;
}
char getTurn(pair<int,int> original, pair<int,int> next){
    if (abs(original.first - next.first) == 1)
        return original.first - next.first == 1 ? 'G' : 'D';
    else if (abs(original.second - next.second) == 1){
        return original.second - next.second == 1 ? 'L' : 'P';
    }
    else
        return 'S';
}

string getPath(pair<int,int> start, field *fields[]){
    string res;
    while(start.first != -1 && start.second != -1){
        res += getTurn(fields[start.first][start.second].precursor,start);
        start = fields[start.first][start.second].precursor;
    }
    res = res.substr(0,res.size()-1);
    reverse(res.begin(),res.end());
    return res;
}

vector<string> getResult(char *grid[],map<char, drone> robots,int N,int n, int m){
    queue<pair<int, int> > q;
    map<char, drone>::iterator it;
    //Array of size of the entry grid to move our bots and backtrack movements for answers.

    field **moves;
    moves = new field *[n];
    for(int i=0;i< n;i++){
        moves[i] = new field [m];
        for(int j=0;j<m;j++){
            moves[i][j].distance = 100000;
            moves[i][j].precursor = {-1,-1};
        }
    }

    for(it = robots.begin(); it!=robots.end(); it++){
        q.push(it->second.start);
        moves[it->second.start.first][it->second.start.second].distance = 0;

    }

    while(!q.empty()){
        pair<int, int> field = q.front();
        q.pop();

        vector<pair<int,int> > possible = checkFields(grid,field,n,m);
        for(auto & i : possible){
            if(moves[i.first][i.second].distance > moves[field.first][field.second].distance + 1){
                moves[i.first][i.second].distance = moves[field.first][field.second].distance + 1;
                moves[i.first][i.second].precursor = field;
                q.push(i);
            }
        }
    }

    vector<string> paths;
    for(it = robots.begin(); it!=robots.end(); it++){
        paths.push_back(getPath(it->second.end, moves));
    }

    return paths;
}



vector<string> prepareGrid(char *grid[],int N,int n, int m){
    map<char, drone> robots;
    map<char, drone>::iterator it;
    for(int i=0;i<n;i++){
        for(int j=0;j<m;j++){
            char id = char(tolower(grid[i][j]));
            bool lowerCase = grid[i][j] >= 'a' && grid[i][j] <= 'z';
            bool upperCase = grid[i][j] >= 'A' && grid[i][j] <= 'Z';
            if(upperCase || lowerCase){ //Initializing robots
                drone d;
                if(robots.find(id) == robots.end())
                    d.name = id;
                else
                    d = robots[id];

                if(lowerCase)
                    d.start = {i,j};

                if(upperCase)
                    d.end = {i,j};

                robots[d.name] = d;
            }
            else
                continue;
        }
    }

    return getResult(grid,robots,N,n,m);
}

int main() {
    int n,m,K,D,N;
    string line;

    /*
     * Input consists of:
     * n m - Size of grid (n x m) where drones are placed
     * K - Number of robots present on the map
     * D - Distance kept between robots
     * N - Maximum amount of steps before task is aborted
     *
     * */

    cin>>n>>m;
    cin>>K;
    cin>>D;
    cin>>N;
    char** grid;
    grid = new char*[n];
    for(int i=0;i<n;i++){
        string tmp;
        grid[i] = new char[m];
        cin>>tmp;
        for(int j=0;j<m;j++)
            grid[i][j] = tmp[j];
    }

    vector<string> res = prepareGrid(grid,N,n,m);

    for(auto & re : res)
        cout<<re<<endl;

    return 0;
}
