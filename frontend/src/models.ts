interface Model {
    id: number;
}

class SocialProfile implements Model {
    id: number;
    username: string;
    followers: number;

    constructor(id: number = 0, username: string = 'default username', followers: number = 0) {
        this.id = id; this.username = username; this.followers = followers;
    }
}

class Position {
    lat: number;
    long: number;

    constructor(lat: number = 0.0, long: number = 0.0) {
        this.lat = lat; this.long = long;
    }
}

class Location implements Model {
    id: number;
    name: string;
    position: Position;
    score: number;

    constructor(id: number = 0, name: string = 'default name', position: Position = new Position(0.0, 0.0), score: number = 0.0) {
        this.id = id; this.name = name; this.position = position; this.score = score;
    }
}

class Account {
    accountname: string;
    email: string;
    password: string;
    preference: boolean;
    followers: number;
    remember: boolean;

    constructor(accountname: string = 'default name', email: string = 'default email', password: string = 'default password', 
                preference: boolean = true, followers: number = 0, remember: boolean = false) {
        this.accountname = accountname; this.email = password; this.preference = preference; this.followers = followers; this.remember = remember;
    }
}

class PostScore {
    media_score: number;
    caption_score: number;
}

class Post implements Model {
    id: number;
    caption: string;
    media_url: string;
    profile: SocialProfile;
    location: Location | null;
    score: PostScore | null;
}

export { Account, Post, SocialProfile, Position, Location };
