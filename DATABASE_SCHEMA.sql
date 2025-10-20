-- Database schema for Maalem Platform

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP WITH TIME ZONE,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
    user_type VARCHAR(10) CHECK (user_type IN ('client', 'artisan')) DEFAULT 'client',
    phone_number VARCHAR(15),
    address TEXT,
    profile_picture VARCHAR(100),
    bio TEXT,
    specialty VARCHAR(100),
    experience_years INTEGER,
    rating DECIMAL(3, 2) DEFAULT 0.0,
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6)
);

-- Posts table
CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    author_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    image VARCHAR(100),
    category VARCHAR(100),
    location VARCHAR(200),
    latitude DECIMAL(9, 6),
    longitude DECIMAL(9, 6)
);

-- Likes table
CREATE TABLE likes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, post_id)
);

-- Comments table
CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Saved posts table
CREATE TABLE saved_posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    post_id INTEGER NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    saved_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, post_id)
);

-- Conversations table
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Conversation participants table (many-to-many relationship)
CREATE TABLE conversation_participants (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(conversation_id, user_id)
);

-- Messages table
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE
);

-- Notifications table
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    recipient_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    actor_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    verb VARCHAR(255) NOT NULL,
    description TEXT,
    target_content_type VARCHAR(255),
    target_object_id INTEGER,
    action_object_content_type VARCHAR(255),
    action_object_object_id INTEGER,
    level VARCHAR(20) DEFAULT 'info',
    unread BOOLEAN DEFAULT TRUE,
    public BOOLEAN DEFAULT TRUE,
    deleted BOOLEAN DEFAULT FALSE,
    emailed BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Reviews table
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    artisan_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    client_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(artisan_id, client_id)
);

-- Projects table
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    artisan_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    image VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- Portfolio items table
CREATE TABLE portfolio_items (
    id SERIAL PRIMARY KEY,
    artisan_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    image VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Scheduling table
CREATE TABLE schedules (
    id SERIAL PRIMARY KEY,
    artisan_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    client_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) CHECK (status IN ('pending', 'confirmed', 'completed', 'cancelled')) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Payments table
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    artisan_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    client_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'MAD',
    status VARCHAR(20) CHECK (status IN ('pending', 'completed', 'failed', 'refunded')) DEFAULT 'pending',
    payment_method VARCHAR(50),
    transaction_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Warranty claims table
CREATE TABLE warranty_claims (
    id SERIAL PRIMARY KEY,
    artisan_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    client_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) CHECK (status IN ('submitted', 'in_review', 'approved', 'rejected', 'resolved')) DEFAULT 'submitted',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- Support tickets table
CREATE TABLE support_tickets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    subject VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) CHECK (status IN ('open', 'in_progress', 'resolved', 'closed')) DEFAULT 'open',
    priority VARCHAR(10) CHECK (priority IN ('low', 'medium', 'high', 'urgent')) DEFAULT 'medium',
    category VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Training courses table
CREATE TABLE training_courses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    instructor_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    duration INTEGER, -- in hours
    level VARCHAR(20) CHECK (level IN ('beginner', 'intermediate', 'advanced')),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- User training enrollments table
CREATE TABLE user_training_enrollments (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    course_id INTEGER NOT NULL REFERENCES training_courses(id) ON DELETE CASCADE,
    enrolled_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(user_id, course_id)
);

-- Materials table
CREATE TABLE materials (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    artisan_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Verification requests table
CREATE TABLE verification_requests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    id_document_front VARCHAR(100),
    id_document_back VARCHAR(100),
    status VARCHAR(20) CHECK (status IN ('pending', 'approved', 'rejected')) DEFAULT 'pending',
    reviewed_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    reviewed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for better performance
CREATE INDEX idx_posts_author ON posts(author_id);
CREATE INDEX idx_posts_created_at ON posts(created_at);
CREATE INDEX idx_likes_post ON likes(post_id);
CREATE INDEX idx_likes_user ON likes(user_id);
CREATE INDEX idx_comments_post ON comments(post_id);
CREATE INDEX idx_comments_user ON comments(user_id);
CREATE INDEX idx_saved_posts_user ON saved_posts(user_id);
CREATE INDEX idx_saved_posts_post ON saved_posts(post_id);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_sender ON messages(sender_id);
CREATE INDEX idx_notifications_recipient ON notifications(recipient_id);
CREATE INDEX idx_notifications_unread ON notifications(unread);
CREATE INDEX idx_reviews_artisan ON reviews(artisan_id);
CREATE INDEX idx_reviews_client ON reviews(client_id);
CREATE INDEX idx_projects_artisan ON projects(artisan_id);
CREATE INDEX idx_portfolio_items_artisan ON portfolio_items(artisan_id);
CREATE INDEX idx_schedules_artisan ON schedules(artisan_id);
CREATE INDEX idx_schedules_client ON schedules(client_id);
CREATE INDEX idx_payments_artisan ON payments(artisan_id);
CREATE INDEX idx_payments_client ON payments(client_id);
CREATE INDEX idx_warranty_claims_artisan ON warranty_claims(artisan_id);
CREATE INDEX idx_warranty_claims_client ON warranty_claims(client_id);
CREATE INDEX idx_support_tickets_user ON support_tickets(user_id);
CREATE INDEX idx_user_training_enrollments_user ON user_training_enrollments(user_id);
CREATE INDEX idx_user_training_enrollments_course ON user_training_enrollments(course_id);
CREATE INDEX idx_materials_artisan ON materials(artisan_id);
CREATE INDEX idx_verification_requests_user ON verification_requests(user_id);
CREATE INDEX idx_verification_requests_status ON verification_requests(status);