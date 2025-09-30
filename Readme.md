# K2 Insurance AI Assistant - Intelligence System

## Overview
The K2 Intelligence System is a sophisticated, modular AI-powered solution for insurance data analysis and customer service. It has been completely refactored from a monolithic structure into a clean, maintainable, and scalable architecture.

## Architecture

### 📁 Project Structure
```
src/K2/aims_view/
├── ai/                          # AI/LLM Components
│   ├── __init__.py
│   ├── ssl_config.py           # SSL bypass configuration
│   └── llm_factory.py          # LLM model factory
├── agents/                      # AI Agents
│   ├── intelligence/           # Core intelligence agents
│   │   ├── strategic_planner.py
│   │   ├── query_architect.py
│   │   ├── execution_specialist.py
│   │   ├── computational_analyst.py
│   │   ├── results_evaluator.py
│   │   ├── response_generator.py
│   │   └── schema_analyst.py
│   ├── specialized/            # Specialized agents
│   │   ├── name_detector.py
│   │   ├── customer_validator.py
│   │   └── name_matcher.py
│   └── intelligence_manager.py  # Main orchestrator
├── core/                       # Core functionality
│   ├── __init__.py
│   ├── main.py                 # Main entry point
│   ├── domain_knowledge.py     # AIMS domain knowledge
│   └── interactive.py          # Interactive interfaces
├── utils/                      # Utilities
│   ├── __init__.py
│   ├── query_utils.py          # SQL query utilities
│   └── context_builder.py     # Context building utilities
├── database/                   # Database layer (unchanged)
│   └── database.py
└── config.json                 # Enhanced configuration
```

## Key Components

### 🧠 Intelligence Manager
**Location**: `agents/intelligence_manager.py`

The central orchestrator that coordinates all AI agents to solve complex insurance queries intelligently.

**Features**:
- Multi-cycle problem solving
- Smart retry logic
- Name detection and customer identification
- Strategic planning and execution
- Computational analysis
- Streaming response generation

### 🤖 AI Agents

#### Intelligence Agents
- **Strategic Planner**: Creates execution strategies
- **Query Architect**: Designs optimal SQL queries
- **Execution Specialist**: Handles query execution
- **Computational Analyst**: Performs complex calculations
- **Results Evaluator**: Evaluates query results
- **Response Generator**: Creates final responses
- **Schema Analyst**: Analyzes database schema

#### Specialized Agents
- **Name Detector**: Identifies names in queries
- **Customer Validator**: Validates customer data
- **Name Matcher**: Intelligent name matching

### 🔧 AI Infrastructure
**Location**: `ai/`

- **SSL Config**: Enterprise SSL bypass configuration
- **LLM Factory**: Creates and manages AI model instances
  - Gemini 2.5 Flash for intelligent reasoning
  - Groq LLaMA 3.3 70B for processing
  - Streaming capabilities

### 📚 Domain Knowledge
**Location**: `core/domain_knowledge.py`

Comprehensive AIMS database knowledge including:
- Organizational structure (5 branches, 32 offices)
- Business rules and field patterns
- Critical search patterns
- Financial calculations (loss ratios, etc.)
- 200+ database fields and relationships

### 🛠️ Utilities
**Location**: `utils/`

- **Query Utils**: SQL cleaning, validation, formatting
- **Context Builder**: AI context building utilities

## Usage

### Command Line Interface

```bash
# Interactive mode (default)
python src/K2/aims_view/core/main.py

# Demo mode
python src/K2/aims_view/core/main.py demo

# Explicit interactive mode
python src/K2/aims_view/core/main.py interactive
```

### Environment Variables Required

```bash
export GEMINI_API_KEY="your_gemini_api_key"
export GROQ_API_KEY="your_groq_api_key"
export DB_SERVER_CORE="your_oracle_server"
export DB_SERVICE_CORE="your_oracle_service"
export DB_USER_CORE="your_db_user"
export DB_PASSWORD_CORE="your_db_password"
export DB_PORT_CORE="1521"
```

### Configuration

The system is configured via `config.json` with sections for:

- **AI Models**: Gemini and Groq configurations
- **Intelligence Manager**: Cycle limits, thresholds
- **Agents**: Router and tool configurations
- **Database**: Oracle connection settings

## Key Features

### 🔍 Intelligent Query Processing
- Natural language to SQL conversion
- Multi-step query planning
- Domain-aware field selection
- Business rule application

### 📊 Advanced Analytics
- Loss ratio calculations
- Trend analysis
- Statistical computations
- Comparative analysis

### 🛡️ Enterprise Security
- Input validation and sanitization
- SQL injection prevention
- Rate limiting
- SSL bypass for enterprise environments

### 🌐 Multilingual Support
- Arabic and English language support
- Unicode text handling
- Cultural name variations

### 📈 Real-time Streaming
- Live response generation
- Progress indicators
- Real-time feedback

## Migration from Legacy System

The system has been completely refactored from the original `test.py` (3600+ lines) into a modular architecture:

### Benefits
- **Maintainability**: Clear separation of concerns
- **Scalability**: Easy to add new agents and features
- **Testability**: Individual components can be tested
- **Readability**: Much easier to understand and modify
- **Extensibility**: New AI agents can be added easily

### Backward Compatibility
- All original functionality is preserved
- Same API endpoints and interfaces
- Same configuration options
- Enhanced with new features

## Development

### Adding New Agents
1. Create agent class in appropriate subfolder
2. Implement `get_agent()` method
3. Add to intelligence manager
4. Update configuration as needed

### Extending Domain Knowledge
1. Update `core/domain_knowledge.py`
2. Add new business rules or field patterns
3. Update context builders as needed

### Adding New AI Models
1. Update `ai/llm_factory.py`
2. Add model configuration to `config.json`
3. Update agents to use new models

## Performance Optimizations

- **Parallel Tool Calls**: Multiple operations executed simultaneously
- **Smart Caching**: Schema and domain knowledge caching
- **Connection Pooling**: Efficient database connections
- **Streaming Responses**: Real-time user feedback
- **Retry Logic**: Automatic error recovery

## Monitoring and Logging

- Comprehensive logging throughout system
- Performance metrics tracking
- Error handling and recovery
- Debug mode support

## Security Features

- Enterprise SSL bypass configuration
- Input validation and sanitization
- SQL injection prevention
- Rate limiting and throttling
- Secure credential management

This modular architecture provides a solid foundation for future enhancements while maintaining all the sophisticated AI capabilities of the original system.
