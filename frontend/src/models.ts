interface Model {
    id: number;
}

export class SocialProfile implements Model {
    id: number;
    username: string;
    followers: number;

    constructor(id: number = 0, username: string = 'default username', followers: number = 0) {
        this.id = id; this.username = username; this.followers = followers;
    }
}

export class Position {
    lat: number;
    long: number;

    constructor(lat: number = 0.0, long: number = 0.0) {
        this.lat = lat; this.long = long;
    }
}

export class Location implements Model {
    id: number;
    name: string;
    position: Position;
    score: number;

    constructor(id: number = 0, name: string = 'default name', position: Position = new Position(0.0, 0.0), score: number = 0.0) {
        this.id = id; this.name = name; this.position = position; this.score = score;
    }
}

export class Account {
    accountname: string;
    email: string;
    preference: boolean;

    constructor(accountname: string = 'default name', email: string = 'default email', preference: boolean = true) {
        this.accountname = accountname; this.email=email; this.preference = preference;
    }
}

class PostScore {
    media_score: number;
    caption_score: number;
}

export class Post implements Model {
    id: number;
    caption: string;
    media_url: string;
    profile: SocialProfile;
    location: Location | null;
    score: PostScore | null;
}

export class Info {
    name: string; 
    img: any;
    address: string;
    score: number;

    constructor(name: string, img: any, address:string, score:number) {this.name=name; this.img=img; this.address=address; this.score=score;}
}

export class Filter {
    only_from_followed: boolean;
    lat: number;
    long: number;
    current_lat: number;
    current_long: number;
    radius: number;
    min_rating: number;

    constructor(only_from_followed: boolean=false, lat: number=null, long: number=null, current_lat: number=null, current_long: number=null, radius: number=null, min_rating: number=0.0) {
        this.only_from_followed=only_from_followed; this.lat=lat; this.long=long; this.current_lat=current_lat; this.current_long=current_long; this.radius=radius; this.min_rating=min_rating;
    }
}