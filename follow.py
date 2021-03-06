from pymongo.errors import ConnectionFailure
import sys

def followInterface(db, user):
    switch = {1:follow, 2:unfollow, 3:following, 4:followers, 5:banfollow}
    switchnum = None
    while switchnum not in {'0'}:
        print("=============================================")
        print("1. 팔로우하기")
        print("2. 언팔로우하기")
        print("3. 내가 팔로우하고 있는 사람들 확인하기")
        print("4. 나를 팔로우하고 있는 사람들 확인하기")
        print("5. 차단하기")
        print("0. 종료하기")

        switchnum =input("뭐할래? 번호를 입력해라: ")
        try:
            if eval(switchnum) in {1, 2, 3, 4, 5}:
                return switch[eval(switchnum)](db, user)
            if eval(switchnum) == 0:
                return
            else:
                print("있는 것 중에 똑바로 선택해라")
        except:
            print("있는 것 중에 똑바로 선택해라")



def following(db, user):
    try:
        res = list(db.follow.find({"follower":user['uid']}))
        if not res:
            print("팔로우하는 사람 없음")
            return followInterface(db, user)
        else:
            print("너가 팔로우하는 사람들")
            for idx in range(len(res)):
                one = res[idx]
                print("["+str(idx+1)+"]", one['following'])
            return followInterface(db, user)

    except:
        print("에러")


def followers(db, user):
    try:
        res = list(db.follow.find({"following":user['uid']}))
        if not res:
            print("너를 팔로우하는 사람 아무도 없음")
        else:
            print("너를 팔로우하는 이상한 애들:")
            for idx in range(len(res)):
                one = res[idx]
                print("["+str(idx+1)+"]", one['follower'])
    except:
        print("error")
    finally:
        return followInterface(db, user)


def follow(db, user):
    while True:
        wantfollow = input("팔로우 하고 싶은 사람의 id를 알려줘(뒤로가고 싶으면 엔터키):")
        if not wantfollow:
            return followInterface(db, user)
        else:
            try:
                cur = db.users.find_one({"uid": wantfollow})
                if not cur:
                    print("그런 유저 없다")
                if cur:
                    res = db.follow.find_one({"follower":user['uid'], "following":wantfollow})
                    if res:
                        print("이미 팔로우 하고 있잖아!")
                    else:
                        db.follow.insert_one({"follower":user['uid'], "following":wantfollow})
                        print("팔로우 성공>_<")
                        followInterface(db, user)

            except Exception as e:
                sys.stderr.write("could not operate following %s\n" %e)
            '''
            1. 팔로우하고자 하는 유저가 존재하는지 확인, 없으면 경고 출력

            2. 팔로우하고자 하는 유저가 나의 팔로잉 목록에 있는지 확인, 있으면 경고 출력

            3. 팔로잉 목록에 없으면,
                나의 팔로잉 목록에 팔로우할 유저id 추가 + 상대방의 팔로워 목록에 내 id 추가
            '''

def unfollow(db, user):
    '''
            1. 언팔로우하고자하는 유저가 존재하는지 확인, 없으면 경고 출력

            2. 언팔로우하고자 하는 유저가 나의 팔로잉 목록에 있는지 확인, 없으면 경고 출력

            3. 팔로잉 목록에 있으면,
                나의 팔로잉 목록에서 언팔로우할 유저id 제거 + 상대방의 팔로워 목록에서 내 id 제거
    '''

    res = list(db.follow.find({"follower": user['uid']}))
    if not res:
        print("팔로우하는 사람 없음")
    else:
        print("너가 팔로우하는 사람들")
        for idx in range(len(res)):
            one = res[idx]
            print("[" + str(idx + 1) + "]", one['following'])
        while True:
            unfoll = input("언팔로우 할 유저의 아이디를 입력해라(뒤로가고 싶으면 엔터키):")
            if unfoll:
                try:
                    cur = db.users.find_one({"uid": unfoll})
                    if not cur:
                        print("그런 유저 없다")
                    else:
                        res = db.follow.find_one({"follower": user['uid'], "following": unfoll})
                        if res:
                            conf0 = input(str(unfoll) + "확실해? 확실하면 y를 입력해라: ").lower()
                            if conf0 == 'y':
                                db.follow.delete_one({"follower":user['uid'], "following":unfoll})
                                print("언팔로우 성공>_<")
                                return followInterface(db, user)

                finally:
                    pass
            else:
                return followInterface(db, user)



def banfollow(db, user):
        res = list(db.follow.find({"following":user['uid']}))
        if not res:
            print("너를 팔로우하는 사람 아무도 없는데 차단은 무슨")
            return followInterface(db, user)
        else:
            while True:
                banfoll = input("차단할 유저의 아이디를 입력해라(뒤로가고 싶으면 엔터키):")
                if banfoll:
                    #try:
                        cur = db.users.find_one({"uid": banfoll})
                        if not cur:
                            print("그런 유저 없다")
                        else:
                            res = db.follow.find_one({"follower": banfoll, "following": user['uid']})
                            if res:
                                conf0 = input("'"+str(banfoll)+"'" + " 확실해? 확실하면 y를 입력해라: ").lower()
                                if conf0 == 'y':
                                    db.follow.delete_one({"follower": banfoll, "following": user['uid']})
                                    print("차단 성공!>.<")
                            else:
                                print("그 사람 너 팔로우 안하는데?")


                   # except:
                       # print("error")
                else:
                    return followInterface(db, user)

