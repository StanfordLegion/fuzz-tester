#ifndef __RANDOM_MAPPER_H__
#define __RANDOM_MAPPER_H__

#include "legion.h"

using namespace LegionRuntime::HighLevel;

void register_random_mappers(Machine, HighLevelRuntime*,
                             const std::set<Processor>&);

#endif // __RANDOM_MAPPER_H__
