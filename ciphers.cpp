//Course Number:	CIS4362
//Course Name:		Cryptology
//Assignment Name:	Multi Cipher
//My Name:			Stephen Wehlburg
//Date:				December 10th 2020
#include <cstdint>
#include <vector>
#include <set>
#include <iostream>

using namespace std;

int get_val(char ch)
{
    if ((65 <= ch) && (ch <= 73))
    {
        return ch - 65;
    }
    else if  ((74 <= ch) && (ch <= 90))
    {
        return ch - 66;
    }
    else
    {
        return -1;
    }
}


char get_char(int num)
{
    if ((0 <= num) && (num <= 7))
    {
        return 65 + num;
    }
    else if ((8 <= num) && (num <= 25))
    {
        return 66 + num;
    }
    else
    {
        return -1;
    }
}

extern "C"
{
    void rail_fence(const char *msg, char *buffer, int msg_len, int rails);
    void caesar(const char *msg, char *buffer, int msg_len, int rotate);
    void trans(const char *msg, char *buffer, int msg_len, const char *key, int key_len);
    void four(const char *msg, char *buffer, int msg_len, const char *key1, int key1_len, const char* key2, int key2_len);
}

void rail_fence(const char *msg, char *buffer, int msg_len, int num_rails)
{
    if(num_rails == 1)
    {
        for(int i = 0; i < msg_len; ++i)
        {
            buffer[i] = msg[i];
        }
    }
    else
    {
        vector<vector<char>> rails;
        vector<int> real_lengths;
        for(int i = 0; i < num_rails; ++i)
        {
            vector<char> temp;
            rails.push_back(temp);
            real_lengths.push_back(0);
        }

        int cur_rail = 0;
        bool down = true;
        for(int i = 0; i < msg_len-1; ++i)
        {
            rails[cur_rail].push_back(msg[i]);
            real_lengths[cur_rail] = real_lengths[cur_rail] + 1;

            if(down) { ++cur_rail; }
            else { --cur_rail; }

            if(cur_rail == 0) { down = true; }
            else if(cur_rail == (num_rails - 1)) { down = false; }
        }

        int final_length = 0;
        for(int i = 0; i < num_rails; ++i)
        {
            for(int j = 0; j < real_lengths[i]; ++j)
            {
                buffer[final_length] = rails[i][j];
                ++final_length;
            }
        }
    }
}

void caesar(const char *msg, char *buffer, int msg_len, int rotate)
{
    for(int i = 0; i < msg_len; ++i)
    {
        int val = get_val(msg[i]);
        if(val != -1)
        {
            buffer[i] = get_char((val + rotate) % 25);
        }
        else
        {
            buffer[i] = msg[i];
        }
    }
}

void trans(const char *msg, char *buffer, int msg_len, const char *key, int key_len)
{
    vector<vector<char>> cols;
    vector<int> vals;
    key_len = key_len - 1;

    for(int i = 0; i < key_len; ++i)
    {
        vector<char> temp;
        cols.push_back(temp);
        vals.push_back(get_val(key[i]));
    }

    for(int i = 0; i < msg_len-1; ++i)
    {
        cols[i % key_len].push_back(msg[i]);
    }

    int index = 0;
    for(int i = 0; i < key_len; ++i)
    {
        int low_val = 30;
        int low_index = -1;
        for(int j = 0; j < key_len; ++j)
        {
            if(vals[j] < low_val)
            {
                low_val = vals[j];
                low_index = j;
            }
        }
        for(int j = 0; j < cols[low_index].size(); ++j)
        {
            buffer[index] = cols[low_index][j];
            ++index;
        }
        vals[low_index] = 29;
    }
}

void four(const char *msg, char *buffer, int msg_len, const char *key1, int key1_len, const char* key2, int key2_len)
{
    int index = 0;
    set<int> grid1set;
    vector<vector<int>> grid1;

    for(int i = 0; i < 5; i++)
    {
        vector<int> temp;
        grid1.push_back(temp);
    }
    for(int i = 0; i < key1_len; ++i)
    {
        if(get_val(key1[i]) != -1 && grid1set.find(get_val(key1[i])) == grid1set.end())
        {
            grid1set.insert(get_val(key1[i]));
            grid1.at(index/5).push_back(get_val(key1[i]));
            index += 1;
        }
    }
    for(int i = 0; i < 25; ++i)
    {
        if(grid1set.find(i) == grid1set.end())
        {
            grid1set.insert(i);
            grid1.at(index/5).push_back(i);
            index += 1;
        }
    }

    index = 0;
    set<int> grid2set;
    vector<vector<int>> grid2;
    for(int i = 0; i < 5; i++)
    {
        vector<int> temp;
        grid2.push_back(temp);
    }
    for(int i = 0; i < key2_len; ++i)
    {
        if(get_val(key2[i]) != -1 && grid2set.find(get_val(key2[i])) == grid2set.end())
        {
            grid2set.insert(get_val(key2[i]));
            grid2.at(index/5).push_back(get_val(key2[i]));
            index += 1;
        }
    }
    for(int i = 0; i < 25; ++i)
    {
        if(grid2set.find(i) == grid2set.end())
        {
            grid2set.insert(i);
            grid2.at(index/5).push_back(i);
            index += 1;
        }
    }

    int val1 = 0;
    int val2 = 0;
    index = 0;
    for(int i = 0; i < msg_len; i += 2)
    {
        while(get_val(msg[i]) == -1)
        {
            i++;
        }
        if(!(i+1 < msg_len))
        {
            break;
        }
        val1 = get_val(msg[i])/5;
        while(get_val(msg[i+1]) == -1)
        {
            i++;
        }
        if(!(i+1 < msg_len))
        {
            break;
        }
        val2 = get_val(msg[i+1])%5;
        buffer[index] = get_char(grid1.at(val1).at(val2));
        ++index;

        val1 = get_val(msg[i])%5;
        while(get_val(msg[i]) == -1)
        {
            i++;
        }
        if(!(i+1 < msg_len))
        {
            break;
        }
        val2 = get_val(msg[i+1])/5;
        while(get_val(msg[i+1]) == -1)
        {
            i++;
        }
        if(!(i+1 < msg_len))
        {
            break;
        }
        buffer[index] = get_char(grid2.at(val1).at(val2));
        ++index;
    }

    if(msg_len % 2 == 1)
    {
        buffer[index] = msg[msg_len - 1];
    }
}